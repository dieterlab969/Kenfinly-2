// Exercise this local HTTPS environment; creates only labeled synthetic records.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import dns from 'node:dns/promises';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const tool = path.join(root, 'kenfinly-local');
const output = path.join(root, 'storage/app/kenfinly-local/evidence');
const hostname = 'alpha.my.kenfinly.com';
const origin = `https://${hostname}`;
const nonce = `${Date.now()}-${crypto.randomBytes(3).toString('hex')}`;
const email = `local-${nonce}@example.test`;
const password = `Local-${crypto.randomBytes(18).toString('hex')}!`;
const checks = { timestamp: new Date().toISOString(), syntheticUser: email, tlsVerificationDisabled: false };
fs.mkdirSync(output, { recursive: true, mode: 0o700 });

function local(...arguments_) {
    return execFileSync(tool, arguments_, { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
}

function query(sql) {
    const arguments_ = Buffer.from(JSON.stringify({ query: sql })).toString('base64');
    const response = JSON.parse(local('php', 'artisan', 'boost:execute-tool', 'Laravel\\Boost\\Mcp\\Tools\\DatabaseQuery', arguments_, '--no-interaction'));
    assert.equal(response.isError, false, 'Boost query must succeed');
    return JSON.parse(response.content[0].text);
}

async function until(check, description, timeout = 30000) {
    const deadline = Date.now() + timeout;
    while (Date.now() < deadline) {
        const result = await check();
        if (result) return result;
        await new Promise(resolve => setTimeout(resolve, 200));
    }
    throw new Error(`Timed out: ${description}`);
}

const addresses = await dns.lookup(hostname, { all: true });
assert(addresses.length > 0 && addresses.every(item => ['127.0.0.1', '::1'].includes(item.address)), 'Only local loopback resolution is allowed');
checks.resolution = addresses.map(item => item.address);
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ ignoreHTTPSErrors: false, viewport: { width: 1440, height: 1000 } });
const page = await context.newPage();
const failedAssets = [];
const pageErrors = [];
let workerPaused = false;
let viteStarted = false;
let probePath;
let initialProbe;
let changedProbe;

await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.hostname !== hostname) return route.abort('blockedbyclient');
    return route.continue();
});
page.on('pageerror', error => pageErrors.push(error.message));
page.on('response', response => {
    if (['script', 'stylesheet', 'font', 'image'].includes(response.request().resourceType()) && response.status() >= 400) {
        failedAssets.push({ url: response.url(), status: response.status() });
    }
});

try {
    const response = await page.goto(`${origin}/register`);
    assert.equal(response.status(), 200);
    checks.browserTls = await response.securityDetails();
    await page.locator('#email').fill(email);
    await page.locator('#name').fill(`Local verification ${nonce}`);
    await page.locator('#password').fill(password);
    await page.locator('#password_confirmation').fill(password);
    await page.locator('#tos').check();
    // Defaults were inspected on the actual form: default assets and USD base currency.
    assert.equal(await page.locator('#base_currency').inputValue(), 'USD');
    await page.getByRole('button', { name: 'Register', exact: true }).click();
    await page.waitForURL(`${origin}/`);
    checks.registration = 'passed';
    const cookies = await context.cookies(origin);
    const session = cookies.find(cookie => cookie.name === '__Host-kenfinly_alpha_session');
    assert(session && session.secure && session.httpOnly && session.domain === hostname && session.path === '/');
    assert.equal((await context.cookies('https://my.kenfinly.com')).length, 0, 'No local cookies must be sent to production');
    checks.session = { name: session.name, domain: session.domain, secure: session.secure, httpOnly: session.httpOnly, sameSite: session.sameSite, productionCookieCount: 0 };

    let csrf = await page.locator('meta[name="csrf-token"]').getAttribute('content');
    const requestHeaders = () => ({ 'X-CSRF-TOKEN': csrf, Origin: origin, Referer: `${origin}/`, Accept: 'application/json' });
    // Use a fresh browser session for login checks; logout is not a prerequisite.
    await context.clearCookies();
    await page.goto(`${origin}/login`);
    await page.locator('#email').fill(email);
    await page.locator('#password').fill('deliberately-incorrect-local-password');
    await page.locator('#login').click();
    await page.locator('.invalid-feedback').first().waitFor();
    assert(page.url().includes('/login'));
    checks.wrongPasswordRejected = true;
    await page.locator('#password').fill(password);
    await page.locator('#login').click();
    await page.waitForURL(`${origin}/`);
    csrf = await page.locator('meta[name="csrf-token"]').getAttribute('content');
    checks.login = 'passed';

    const user = query(`SELECT id FROM users WHERE email = '${email}'`)[0];
    const currency = query(`SELECT id FROM currencies WHERE user_id = ${user.id} AND base = 1`)[0];
    const group = query(`SELECT id FROM account_groups WHERE user_id = ${user.id} ORDER BY id LIMIT 1`)[0];
    assert(currency && group, 'Registration must initialize currency and account groups');
    const payeeResponse = await context.request.post(`${origin}/api/v1/payees`, {
        headers: requestHeaders(), data: { name: `Local merchant ${nonce}`, active: true, config_type: 'payee', config: { category_id: null } },
    });
    assert.equal(payeeResponse.status(), 201, await payeeResponse.text());
    const payee = await payeeResponse.json();
    const walletName = `Local wallet ${nonce}`;
    const walletResponse = await context.request.post(`${origin}/account-entity?type=account`, {
        headers: requestHeaders(), maxRedirects: 0,
        data: { name: walletName, active: true, config_type: 'account', config: { opening_balance: '500.00', account_group_id: group.id, currency_id: currency.id } },
    });
    assert.equal(walletResponse.status(), 302);
    const wallet = query(`SELECT id FROM account_entities WHERE user_id = ${user.id} AND name = '${walletName}'`)[0];
    checks.wallet = { id: wallet.id, openingBalance: '500.00', currency: 'USD' };
    const missingCsrf = await context.request.post(`${origin}/account-entity?type=account`, { data: { name: 'Must not be created' }, headers: { Accept: 'application/json' } });
    assert.equal(missingCsrf.status(), 419, 'Missing CSRF must be rejected');
    checks.csrfRejection = 419;

    for (const [type, amount, from, to] of [['deposit', '150.00', payee.id, wallet.id], ['withdrawal', '30.00', wallet.id, payee.id]]) {
        const result = await context.request.post(`${origin}/api/v1/transactions/standard`, {
            headers: requestHeaders(), data: { action: 'create', transaction_type: type, config_type: 'standard',
                date: new Date().toISOString().slice(0, 10), comment: `Local HTTPS verification ${nonce}`, schedule: false, reconciled: false,
                config: { account_from_id: from, account_to_id: to, amount_from: amount, amount_to: amount }, items: [] },
        });
        assert.equal(result.status(), 200, await result.text());
        const body = await result.json();
        checks[type] = { id: body.transaction.id, amount: body.transaction.config.amount_from };
    }

    local('worker', 'stop');
    workerPaused = true;
    const queued = await context.request.post(`${origin}/api/v1/accounts/${wallet.id}/monthly-summary`, { headers: requestHeaders() });
    assert.equal(queued.status(), 202, await queued.text());
    checks.pendingJobsBeforeWorker = Number(query('SELECT COUNT(*) AS count FROM jobs')[0].count);
    assert(checks.pendingJobsBeforeWorker > 0, 'Existing summary operation must enqueue real work');
    checks.openingSummaryWorkaround = 'Existing full summary endpoint used; known Day 02 initialization defect is not fixed';
    local('worker', 'start');
    workerPaused = false;
    const balance = await until(async () => {
        const result = await context.request.get(`${origin}/api/v1/accounts/${wallet.id}/balance`, { headers: requestHeaders() });
        assert.equal(result.status(), 200);
        const body = await result.json();
        return body.result === 'success' && body.accountBalanceData?.[0]?.cash === 620 ? body : false;
    }, 'database worker calculates the existing summary');
    checks.nativeBalance = balance.accountBalanceData[0].cash;
    checks.backgroundSummary = 'processed';

    await page.waitForLoadState('networkidle');
    local('restart');
    await page.goto(`${origin}/account-entity/${wallet.id}?type=account`);
    assert.equal(new URL(page.url()).hostname, hostname);
    assert(!page.url().includes('/login'), 'Session and key must survive app restart');
    csrf = await page.locator('meta[name="csrf-token"]').getAttribute('content');
    const persisted = await context.request.get(`${origin}/api/v1/transactions/${checks.withdrawal.id}`, { headers: requestHeaders() });
    assert.equal(persisted.status(), 200);
    assert.equal((await persisted.json()).transaction.config.amount_from, '30.0000');
    checks.persistenceAfterRestart = 'passed';
    await page.screenshot({ path: path.join(output, 'wallet-https.png'), fullPage: true });

    const mailResponse = await context.request.post(`${origin}/password/email`, { headers: requestHeaders(), data: { email } });
    assert.equal(mailResponse.status(), 200, await mailResponse.text());
    const message = await until(async () => {
        const messages = await (await fetch('http://127.0.0.1:18025/api/v1/messages')).json();
        return messages.messages?.find(item => item.To?.some(recipient => recipient.Address === email));
    }, 'synthetic password-reset email arrives only in local Mailpit');
    checks.mailCapture = { subject: message.Subject, recipient: email, transport: 'isolated loopback Mailpit; no relay/forwarding configured' };

    const relativeProbe = `resources/js/kenfinly-local-hmr-${nonce}.js`;
    probePath = path.join(root, relativeProbe);
    initialProbe = `export const value = 'initial';
window.__kenfinlyHmr = value;
if (import.meta.hot) {
    import.meta.hot.accept(module => { window.__kenfinlyHmr = module.value; });
}
`;
    changedProbe = initialProbe.replace("'initial'", "'updated'");
    fs.writeFileSync(probePath, initialProbe, { flag: 'wx' });
    local('dev', 'start');
    viteStarted = true;
    const secureSockets = [];
    page.on('websocket', websocket => secureSockets.push(websocket.url()));
    await page.goto(`${origin}/`);
    await page.waitForFunction(() => [...document.scripts].some(script => script.src.includes(':15173/@vite/client')));
    await page.evaluate(url => import(url), `https://${hostname}:15173/${relativeProbe}`);
    await page.waitForFunction(() => window.__kenfinlyHmr === 'initial');
    await page.waitForLoadState('networkidle');
    await until(() => secureSockets.some(url => url.startsWith(`wss://${hostname}:15173/`)), 'secure HMR socket connects before editing');
    assert.equal(fs.readFileSync(probePath, 'utf8'), initialProbe, 'Never overwrite another editor change');
    fs.writeFileSync(probePath, changedProbe);
    await page.waitForFunction(() => window.__kenfinlyHmr === 'updated');
    assert(secureSockets.some(url => url.startsWith(`wss://${hostname}:15173/`)), 'HMR must use a secure WebSocket');
    checks.hmr = { hotUpdate: 'observed initial → updated', secureWebSocket: true, port: 15173 };
    local('dev', 'stop');
    viteStarted = false;
    await page.goto(`${origin}/`);
    await page.waitForLoadState('networkidle');
    assert(!await page.locator('script[src*="15173"]').count(), 'Build mode must be restored after HMR stops');
    assert.equal(failedAssets.length, 0, JSON.stringify(failedAssets));
    assert.equal(pageErrors.length, 0, JSON.stringify(pageErrors));
    checks.assets = 'bundled assets and HTTPS dev modules loaded without failed responses';
    await page.screenshot({ path: path.join(output, 'dashboard-https.png'), fullPage: true });
    checks.status = 'passed-with-documented-opening-summary-workaround';
    fs.writeFileSync(path.join(output, 'synthetic-login.json'), JSON.stringify({ email, password }), { mode: 0o600 });
} catch (error) {
    checks.status = 'failed';
    checks.error = error.message.split('Call log:')[0].trim().slice(0, 2000);
    await page.screenshot({ path: path.join(output, 'verification-failure.png'), fullPage: true }).catch(() => {});
    process.exitCode = 1;
} finally {
    if (workerPaused) local('worker', 'start');
    if (viteStarted) local('dev', 'stop');
    if (probePath && fs.existsSync(probePath)) {
        const contents = fs.readFileSync(probePath, 'utf8');
        if ([initialProbe, changedProbe].includes(contents)) fs.unlinkSync(probePath);
    }
    fs.writeFileSync(path.join(output, 'verification.json'), JSON.stringify(checks, null, 2), { mode: 0o600 });
    await browser.close();
    console.log(JSON.stringify(checks, null, 2));
}
