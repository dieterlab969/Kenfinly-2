# KENFINLY 2.0 — Branding Specification

Date: 2026-11-16\
Baseline: `e3936669c7906550024f56e61aca80cf0d834da8`\
Status: Specification only; runtime graphics and copy have not been changed.

## 1. Brand identity

| Element | Specification |
| --- | --- |
| Product brand / wordmark | `KENFINLY` |
| Product generation | `Kenfinly 2.0` in planning/product documentation; not an instruction to change upstream software or API version numbers |
| Tagline | `Know Your Money.` — preserve capitalization and final period |
| Application display name | `KENFINLY` |
| Logo accessible name | `KENFINLY logo` where the image conveys identity; use empty alt text only when truly decorative and the adjacent wordmark already provides the name |
| Default browser title | `KENFINLY` |
| Page browser title | `KENFINLY - <existing localized page title>` using the existing postfix convention |
| Description | `KENFINLY — Know Your Money. A personal finance application.` |
| Upstream attribution | `Based on YAFFA by Gergely Kántor and contributors. Licensed under the MIT License.` with links to upstream and the retained license |

Use the approved brand spelling across existing languages. Keep the tagline in English in this first stage; localized taglines require an explicit product decision. Ordinary explanatory text remains localized. Do not claim bank connectivity, guaranteed financial accuracy, a production service or an available Kenfinly mobile app.

## 2. Current surfaces and target behavior

| Surface / files | Existing behavior | Target |
| --- | --- | --- |
| `resources/views/template/master.blade.php` | Hard-coded YAFFA default title, existing page postfix, white theme color, favicon under `images/` | KENFINLY default title and agreed description/application-name metadata; retain charset, viewport, CSRF and existing postfix logic |
| `resources/views/template/layouts/page.blade.php` | YAFFA name and 44px logo in navigation; `app.name` footer links to yaffa.cc; GitHub icon links upstream | KENFINLY name/logo in the same layout; preserve visible YAFFA attribution and explicitly labeled upstream links |
| `resources/views/auth/login.blade.php`, `two-factor-challenge.blade.php` | YAFFA logo/name and tracker sentence | KENFINLY wordmark with `Know Your Money.`; preserve the forms, routes, 2FA behavior and registration availability |
| `resources/views/auth/register.blade.php` | Product name in setup instructions/tooltips | KENFINLY display copy, without changing account creation or seeded defaults |
| `resources/views/pages/dashboard.blade.php`, `resources/js/dashboard/components/Dashboard.vue` | YAFFA welcome/onboarding text | KENFINLY welcome/onboarding text; preserve widget calculations and conditions |
| `resources/js/user/UserSettings.vue` | Name in labels and explanations alongside `window.YAFFA` state | KENFINLY display text; keep state keys, ranges and settings behavior |
| `resources/js/user/ApiTokenManager.vue` | YAFFA API/client text and pairing instructions | Identify the KENFINLY API interface; keep YAFFA client references where they accurately describe the compatible client. Do not relabel an existing YAFFA client as a delivered Kenfinly app |
| `lang/{en,fr,hu,pl}.json` | English literal translation keys plus semantic keys | Change selected visible keys/values with callers in all four languages. Retain exact technical identifiers and fixture credentials |
| `resources/views/pages/sandbox-terms.blade.php` | YAFFA instance identity and disclaimer | Identify a Kenfinly test instance only where applicable; retain disclaimer and clearly label upstream documentation |
| `app/Notifications/LoginSuccessNotification.php`, `LoginFailedNotification.php` | YAFFA prefixes in subjects | `KENFINLY info - successful login` and `KENFINLY alert - failed login notification`; preserve recipients and dispatch |
| `resources/views/emails/*.blade.php` | Signatures use `config('app.name')` | Show KENFINLY via reviewed display configuration; verify password reset/verification and other inherited framework mails too |
| `.env.example`, `.env.ci`, `.env.dusk.ci` | `APP_NAME=YAFFA`; example has `MAIL_FROM_NAME=YAFFA` | Review display values for KENFINLY only after checking derived defaults; retain operational variable names and values |
| API docs presentation (`config/scramble.php`) | UI title is null; description/provider metadata supplied elsewhere | Verify installed-package behavior, then set only presentation title if required; preserve auth gates, version and API schemas |
| `README.md` | Upstream project introduction | KENFINLY identity, exact tagline and explicit original project attribution — implemented on Day 01 |

## 3. Assets

No approved KENFINLY artwork has been supplied or created today. Use an original wordmark/icon approved by the Product Owner; do not recolor the YAFFA logo and assume it is a new owned mark. The palette and typography below are deliberately constrained to the existing UI until visual identity is approved.

| Asset | Audited baseline | Initial target |
| --- | --- | --- |
| `public/images/logo-small.png` | 44 × 44 RGB PNG | KENFINLY icon at the same consumed path, 44 × 44 logical pixels; verify sharpness and light/dark backgrounds |
| `public/images/favicon.ico` | One 32 × 32, 24-bit icon; explicitly linked in master layout | KENFINLY ICO at the same path; retain 32px support, optionally include 16px and 48px variants within the file |
| `public/favicon.ico` | Empty tracked file | Same approved KENFINLY favicon for browsers that request the root path |
| `public/vendor/telescope/favicon.ico`, `public/images/vendor/**` | Third-party assets | Preserve; do not apply product-brand replacement to vendor assets |

Retain the current Bootstrap/CoreUI palette, typography and financial chart colors in the first pass. Do not change positive/negative color semantics. A new palette, font, dark-mode redesign or dependency is a separate decision. Maintain existing image slots and layout so the rebrand does not alter transaction forms or reports.

## 4. Metadata and links

Add `application-name=KENFINLY` and the specified description to the shared head after implementation review. The current head has no application description or Open Graph/Twitter tags; no tracked web app manifest or Apple touch icon was found. Existing `public/mix-manifest.json` and the Telescope mix manifest are asset manifests, not PWA manifests.

Retain the current theme color until a new palette is approved. Do not introduce canonical URLs, `og:url`, social image links, manifests, external fonts or analytics without a real approved destination/asset. Open Graph/Twitter cards can be a later display-only addition once those inputs exist; they are not delivered in this stage.

No Kenfinly public domain, support address or sender domain has been approved. In the first pass, the KENFINLY footer name can be plain text; retain an explicitly labeled `YAFFA upstream` link beside attribution. Relabel the login's upstream “Learn more” link as “About YAFFA upstream” until a Kenfinly destination exists. Do not silently repoint all YAFFA documentation links or link KENFINLY text to an assumed domain. Use a named route for any application navigation.

Sender display names may change; SMTP credentials, `MAIL_FROM_ADDRESS`, recipients, DNS, incoming receipt addresses and operational URLs stay unchanged. Existing `.env` values are operator-managed and have not been touched.

## 5. Compatibility exceptions

The following can legitimately remain visible in technical settings, docs or attribution after rebranding:

- YAFFA project credit, upstream repository/docs and original license/copyright notices.
- The existing YAFFA client's name where pairing requires it; literal `yaffa://pair`, `X-Yaffa-Token` and response key `yaffa_version`.
- The exact `yaffa.txt` Google Drive capability-test file. Its name is behavior, not marketing copy.
- Inherited demo/test emails where they are fixture credentials, and upstream sandbox links labeled as upstream.

Internal `config('yaffa.*')`, `window.YAFFA`, namespaces, package names, Docker names and storage/cache keys remain unchanged. A residual-reference search must classify these exceptions; zero matches is not an acceptance target.

## 6. Acceptance criteria

1. Login, registration, password reset, 2FA, application navigation, dashboard, settings, local emails and API docs use the approved display identity wherever applicable.
2. Browser titles retain page context. Both favicon paths serve the approved icon; no broken asset requests appear. Wordmark/alt text are accessible and do not overflow at mobile sizes or in dark mode.
3. Selected display strings and translations are synchronized across English, French, Hungarian and Polish; existing semantic keys and literal protocol/file/fixture values remain intact. Run the repository's translation checker and obtain native review before publication.
4. Technical compatibility exceptions and YAFFA credit remain accurate. Logo replacement does not hide amCharts or other third-party branding/notices.
5. Before/after install, build, test, smoke and rollback evidence satisfy `CHANGE_PLAN.md`. No finance, schema or dependency difference is included.

## 7. Product decisions still needed

- Approve the original icon/wordmark artwork and its rights; retain current palette/font for the first pass or commission a separate design task.
- Confirm the eventual Kenfinly public/support destinations and sender identity before any external link or mail-domain change.
- Confirm how the existing YAFFA mobile client is described until a Kenfinly client exists.
- Approve any Kenfinly-specific terms and any later release/deployment. The engineering plan does not authorize publication.
