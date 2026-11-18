# KENFINLY

**Know Your Money.**

Kenfinly 2.0 is being prepared as a fork of [YAFFA](https://github.com/kantorge/yaffa),
the Yet Another Free Financial Application personal finance application.
The project has isolated Mac development and a public Ubuntu verification deployment.
The application still uses inherited YAFFA UI branding; full display rebranding remains planned.
Deployment was exercised with synthetic data. See the verification record for the opening-summary defect and pending external-email/automatic-trigger checks.

## Original project attribution

YAFFA was created by Gergely Kántor and developed with contributions from the upstream community.
The original project is distributed under the [MIT license](LICENSE), including the original
`Copyright (c) 2021 Gergely Kántor` notice. That license and the existing Git history are preserved.
KENFINLY identifies this downstream product; it does not imply endorsement by the YAFFA maintainers.

- Upstream repository: [kantorge/yaffa](https://github.com/kantorge/yaffa).
- Kenfinly repository: [dieterlab969/Kenfinly-2](https://github.com/dieterlab969/Kenfinly-2).
- Audited starting commit: `e3936669c7906550024f56e61aca80cf0d834da8` on `develop`.
- This clone retains `origin` for Kenfinly and a fetch-enabled `upstream` remote for YAFFA, with its local push URL disabled.
  Remote settings are local to each clone; see [CHANGE_PLAN.md](CHANGE_PLAN.md) for setup instructions.

## Kenfinly rebranding documents

- [Change plan and rollback procedures](CHANGE_PLAN.md)
- [Repository audit](REPOSITORY_AUDIT.md)
- [Branding specification](BRANDING_SPEC.md)
- [License review](LICENSE_REVIEW.md)
- [Day 01 report](DAY_01_REPORT.md)
- [Day 02 local setup and verification report](DAY_02_REPORT.md)
- [Day 03 HTTPS local setup report](DAY_03_REPORT.md)
- [Local onboarding for Apple Silicon](docs/ONBOARDING.md)
- [Local verification evidence and timings](docs/LOCAL_VERIFICATION.md)
- [Latest daily engineering report](DAILY_REPORT.md)

## Public Ubuntu deployment

- [Ubuntu setup and runtime boundaries](docs/UBUNTU_SETUP.md)
- [Network, domain and TLS](docs/NETWORK_AND_DOMAIN.md)
- [Dedicated Jenkins deployment](docs/JENKINS_DEPLOYMENT.md)
- [Deployment and rollback runbook](docs/DEPLOYMENT_RUNBOOK.md)
- [Executed verification and remaining blockers](docs/DEPLOYMENT_VERIFICATION.md)
- [Environment matrix](docs/ENVIRONMENT_MATRIX.md)

## Inherited YAFFA documentation

The sections below describe the upstream application. Links to YAFFA documentation and its sandbox
remain upstream resources; they are not Kenfinly services or a statement of Kenfinly's future roadmap.

**Yet Another Free Financial Application (YAFFA 🍊)**

## About Yaffa

Yaffa is a personal finance web application, focusing on the support of long term financial planning.
Yaffa is a self hosted web application, written in PHP, using Laravel framework.
By hosting your own app instance, your financial data is not uploaded to the cloud, and shared with any third parties.

Read more about YAFFA at https://yaffa.cc

## Key features

- Support multiple currencies.
    - There is a default currency, which is used on dashboards and charts.
    - Currency rates are automatically updated daily.
    - YAFFA utilizes the free Frankfurter service, requiring no API key or registration.
- Support multiple accounts and account groups.
- Track your income and spending by recording transactions.
    - Yaffa tries to come up with suggestions while entering transactions to speed up transaction recording process.
    - Transactions can be split into categories. This helps to better understand spending patterns and budget planning.
    - Yaffa can process documents with AI and prefill transaction details automatically.
        - Supported sources include manual uploads (text/PDF/images), received emails, and Google Drive imports.
        - This feature is optional and currently supports OpenAI or Gemini providers. You need to provide your own API key and billing setup.
        - OCR for images is available via Tesseract (self-hosted) or Vision-capable AI models.
- Scheduled and recurring transactions, and budgets (plans) can be created.
    - This can be used to calculate forecasted data.
    - You can enable the automatic recording of recurring transactions.
- Add your investments, to calculate gain and loss.
    - Automatically retrieve investment prices.
    - This is based on the alphavantage.co service. You need to register and get your free API key.
- Import transactions from QIF and CSV files. Customizable import rules to support country and bank specific formats.

There are several features **planned** to be implemented:

- Further charts, reports and dashboards.
- Handling multiple users as a family in one app instance.
- Better onboarding experience, or a tutorial.

Several features are **not likely to be introduced**, which you might expect from such applications.
If you are looking to have these in a budget app or expense tracker, then YAFFA might not be the best choice for you.

- Downloading transaction data directly from banks
    - The philosophy of expense tracking is to be conscious about your spending and financial habits, which requires the review and manual adjustment of transactions.
      Thus, automatic downloading of transactions from banks would save some time, but would not help to achieve the goal of expense tracking and budgeting.
    - Also, YAFFA supports automatic creation of scheduled transactions and entry of simple recurring transactions, to speed up the process of recording transactions.
- Native mobile app
    - YAFFA is optimized for desktop browsers. The interface is responsive to support mobile view, but not fully optimized for mobile devices.
- YAFFA is a personal finance application, not an accounting application. The precision of the calculations should be sufficient for personal finance, but it is not guaranteed to be accurate enough for accounting purposes. Similarly, the precision is not designed to be sufficient for cryptocurrency transactions and prices.

Read more about the [features of YAFFA](https://yaffa.cc/features-of-yaffa-personal-finance-application/)

## Try it out

You can try out YAFFA without installing it. Take a look at the application at https://sandbox.yaffa.cc

- Do you want to walk around, kick the tires, and see the application in action? Use the demo account featuring realistic sample data.
- Do you want a full test drive to explore the application as if it were your own instance? You can register a new account at https://sandbox.yaffa.cc/register

⚠️ **Important!** This is not a production environment or a free service.
Use it only to experiment with YAFFA's functionality and UI. The database is regularly wiped without prior notice.

💡 **Tip:** use a fake or disposable email address to sign up. The email address does not need to be verified.

## Getting started

Read the full documentation at https://yaffa.cc/documentation/,
including the [Getting Started](https://yaffa.cc/documentation/resources/category/getting-started/) guide
and the [Installation instructions](https://yaffa.cc/documentation/resources/category/installation/).

## Upgrading

When upgrading between major versions, please see the details and follow the instructions listed in the [upgrade guide](UPGRADE.md).

## Contributors

Thanks to these people for helping improve this project:

- [@WMP](https://github.com/WMP) - Polish translation and various features, including the monthly breakdown and drill down functionality.
- [@antmcmullen](https://github.com/antmcmullen) - Performance improvements for the Investments list

## License

YAFFA is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
