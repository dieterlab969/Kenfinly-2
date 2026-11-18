import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { mergeConfig } from 'vite';
import base from '../../vite.config.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const tls = path.join(root, 'storage/app/kenfinly-local/tls');
const hostname = 'alpha.my.kenfinly.com';

export default mergeConfig(base, {
    root,
    server: {
        host: '127.0.0.1',
        port: 15173,
        strictPort: true,
        watch: { ignored: ['**/storage/**', '**/bootstrap/cache/**'] },
        origin: `https://${hostname}:15173`,
        allowedHosts: [hostname],
        cors: { origin: `https://${hostname}` },
        https: {
            cert: fs.readFileSync(path.join(tls, `${hostname}.pem`)),
            key: fs.readFileSync(path.join(tls, `${hostname}-key.pem`)),
        },
        hmr: { host: hostname, protocol: 'wss', clientPort: 15173 },
    },
});
