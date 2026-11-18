# KENFINLY 2.0 — environment matrix

Recorded 2026-11-18 (Asia/Saigon). Application baseline on public Ubuntu: `develop`, `b76d9c6b082bb8de83ab0da29fd58db5af5c2e68`.

| Property | Mac development | Public Ubuntu application | Ubuntu CI |
| --- | --- | --- | --- |
| URL | `https://alpha.my.kenfinly.com` | `https://my.kenfinly.com` | Test-process localhost; no public application |
| Resolution | Mac `/etc/hosts` loopback | Public A → VPS 210.245.84.76 → WireGuard → home | Local executor |
| CPU/OS | Apple M2 arm64, macOS 15.5 | x86_64, Ubuntu 24.04.4 | Same Ubuntu host, Jenkins user |
| PHP | Explicit Homebrew 8.5.6 | Dedicated native PHP/FPM 8.4.27 | Explicit PHP 8.4.27 |
| Node | 26.0.0 / npm 11.12.1 | Built assets; no Vite dev server | Private Node 24.22.3 / npm 11.19.1 |
| Composer | 2.10.0 | Existing 2.7.1 for Linux builds | Existing 2.7.1 through PHP 8.4 |
| MySQL | Isolated 9.6.0 on Mac loopback 13316 | Isolated 8.0.46 on Ubuntu loopback 13316 | Same private Ubuntu instance, separate scoped DB/user |
| Database | `kenfinly_day02` | `kenfinly2` | `kenfinly2_ci` |
| APP_ENV / DEBUG | local / true | production / false | testing / test profile |
| Session cookie | `__Host-kenfinly_alpha_session` | `__Host-kenfinly_public_session` | Array/session test profile |
| Cookie domain | None; host-only alpha | None; host-only public hostname | No real browser shared session |
| TLS | Locally trusted mkcert leaf | Existing public Let's Encrypt leaf on VPS | Tests isolated; public smoke validates real TLS |
| Trusted proxy | No reverse-proxy trust required | Only immediate VPS peer 10.0.0.1 | Existing trusted-proxy tests |
| Mail | Loopback catcher 11025 / UI 18025 | Scoped WireGuard SMTP 10.0.0.1:2525 | Array mailer; synthetic receipt route |
| Verification | Disabled only in local profile | Enabled; signed-link/local VPS delivery tested | Test-only settings |
| Queue/cache/session | DB worker, file cache/session | Owned systemd worker, file cache/session | Sync queue, array cache/session |
| Scheduler | Local owned schedule:work | Single systemd timer / schedule:run | Disabled |
| Source/runtime path | `/Users/dieter/Projects/Kenfinly-2` | Preserved clone `/var/www/Kenfinly-2`; live `/var/www/kenfinly-2-deploy/current` | Dedicated Jenkins workspace |
| Secrets | Ignored Mac `.env` / private storage | Persistent shared `.env`, root-owned private client files | Jenkins secret-file credential `kenfinly2-ci-env` |
| Reset policy | Explicit local-only recipe | Never reset/reseed real/application data | Disposable CI DB refreshed by existing tests |

Never synchronize application keys, `.env`, cookies, real data, CA private keys or installed Mac vendor/node_modules into Ubuntu. Linux dependencies/assets are rebuilt from unchanged lockfiles. Public production cookie selection does not include alpha, and Mac cookie/configuration remains independent.

Ubuntu's selected major runtime matrix matches repository CI (PHP 8.4 / Node 24 / MySQL 8); native installation is not a claim that Sail/container checks ran. Mac's already approved native exception is a different measured matrix. Neither environment received a dependency upgrade or financial/schema source rewrite.

The public environment retains inherited YAFFA UI assets/copy; APP_NAME is KENFINLY. See [DEPLOYMENT_VERIFICATION.md](DEPLOYMENT_VERIFICATION.md) for release limitations, including D02-F01, external email delivery and automatic-trigger verification. Capacity planning/testing was not performed.
