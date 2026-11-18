# KENFINLY 2.0 — License and Attribution Review

Date: 2026-11-16\
Baseline: `e3936669c7906550024f56e61aca80cf0d834da8`\
Scope: Engineering review of the retained project license and dependency metadata; not a completed legal or trademark clearance.

## 1. Original license evidence

The root [LICENSE](LICENSE) contains the MIT License and the original notice:

> Copyright (c) 2021 Gergely Kántor

The fetched upstream `develop` and local starting commit are identical. The [upstream license](https://github.com/kantorge/yaffa/blob/develop/LICENSE) also identifies the project as MIT with that copyright holder. The baseline root license SHA-256 is:

```text
efed17f801214ac1db3f5946e3333a951b9bae6a9b0b9c8547ce81b4def450a3
```

`composer.json` and `package.json` declare MIT for the root application. `LICENSE` is unchanged in this delivery. The original README's contributor acknowledgments and license section remain, with an added downstream attribution section.

## 2. What the project license permits and requires

The MIT text permits use, modification and redistribution, including commercial distribution, subject to retaining its copyright and permission notices in copies or substantial portions. It also disclaims warranties. These obligations follow the software when renamed; rebranding does not transfer original authorship. See the [Open Source Initiative MIT text](https://opensource.org/license/mit).

Engineering policy for this fork:

- Keep the entire original `LICENSE`, including its disclaimer, unchanged in source distributions and release artifacts.
- Keep existing copyright/license headers and third-party notices. Do not replace the original author's name or year with Kenfinly's identity.
- Keep YAFFA attribution and upstream links in README. Git history preservation and README attribution are explicit project requirements in addition to retaining the license notice.
- Any notice for new Kenfinly-authored work must accurately identify an approved legal owner and cover only that new work. No new ownership claim is added today.
- Keep original license declarations in Composer/npm metadata. A future metadata rename requires its own review; no relicensing is proposed.

The MIT software text does not establish trademark clearance for KENFINLY or ownership of new artwork, and this review does not establish an endorsement or affiliation. Those questions remain open product/legal decisions.

## 3. Third-party dependencies require separate attention

Lockfiles were inspected without installing packages. These are locked metadata findings, not conclusions from reviewing every installed package license or the final compiled artifacts.

| Dependency / source | Finding | Required treatment before distribution |
| --- | --- | --- |
| `@amcharts/amcharts4` 4.10.40 | npm lockfile says `SEE LICENSE IN LICENSE` | Inspect the actual license shipped with this exact version and any applicable entitlement. Preserve chart branding/notices; do not assume the application MIT license allows their removal. The vendor's [licensing guidance](https://www.amcharts.com/pricing/licenses-explained/) distinguishes deployment/distribution uses but does not prove this fork has a license. |
| `@fortawesome/fontawesome-free` 6.7.2 | `(CC-BY-4.0 AND OFL-1.1 AND MIT)` | Retain applicable icon/font/code notices; review font/artwork obligations when bundling. |
| `ezyang/htmlpurifier` v4.19.1 | `LGPL-2.1-or-later` | Review the installed license and distribution/source obligations for its actual use; retain notices. |
| `smalot/pdfparser` v2.13.1 | `LGPL-3.0` | Same exact-version/distribution review; no rebranding of its notices. |
| `nette/schema` v1.4.0, `nette/utils` v4.1.6 | Alternative `BSD-3-Clause`, `GPL-2.0-only`, `GPL-3.0-only` entries | Review the actual dual/multiple-license terms and applicable license choice. Do not infer a mandatory GPL choice from the metadata array. |
| `datatables.net-vue3` 3.0.8, `png-js` 1.1.0 | No license field in locked npm package metadata | Inspect distributed license files; missing metadata does not by itself establish that the packages are unlicensed. |
| `rgbcolor` 1.0.1 | `MIT OR SEE LICENSE IN FEEL-FREE.md` | Inspect the exact package notices and license options. |
| Other locked packages and transitive assets | MIT, BSD, Apache, ISC, MPL and other notices are present in metadata | Retain required notices in source/bundles and review actual distribution obligations, including any modifications. |
| `public/vendor/telescope/**`, `public/images/vendor/**` | Third-party published files | Preserve their own assets, branding and notices; exclude them from product-logo replacement. |

The fork also depends on `kantorge/laravel-currency-exchange-rates`, `Kantorge\CurrencyExchangeRates` and a `github:kantorge/datatables-contextual-actions#custom_package` dependency. These are real dependency identities, not residual application branding to rename.

Before the first redistribution, review both production dependencies and the actual release artifact. Include required dependency notices and any source/license materials applicable to that distribution. Do not infer that every package is MIT because the application is MIT. No dependency is added, removed, updated or replaced today.

## 4. Assets and distribution

`public/images/logo-small.png` and `public/images/favicon.ico` are inherited YAFFA assets; the root favicon is empty. No separate asset-specific notice was identified in the tracked asset paths, but that is not proof of a complete rights review. Preserve the inherited files in Git history and replace only application-owned branding with approved original Kenfinly artwork during implementation. Record the artwork's source and rights when it is supplied. Do not modify vendor images, fonts or chart logos to match KENFINLY.

The Dockerfile uses `COPY . .`; `.dockerignore` does not explicitly exclude `LICENSE`. This suggests the root license is copied into the application image, but no image was built or inspected today. Before shipping, inspect the actual image/archive and confirm `LICENSE`, attribution and all required third-party notices are present. Built JS/CSS notice retention has not been verified.

## 5. Review status

| Check | Result |
| --- | --- |
| Original MIT text and copyright identified | Verified from local file and upstream source |
| Original license preserved in worktree | Verified; unchanged hash |
| README attribution and contributors | Preserved/updated explicitly |
| Git ancestry | Preserved; baseline matches fetched upstream |
| Installed dependency licenses | Unverified — `vendor` and `node_modules` absent |
| Final artifact/bundle notice retention | Unverified — no build performed |
| KENFINLY name, artwork and domain clearance | Not established by this review |
| Production or public distribution approval | Not granted or exercised |

Proceed with audit and local preparation. Resolve exact-version dependency/asset obligations and artifact checks before public distribution; no blanket licensing clearance is claimed.
