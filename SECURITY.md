# Security Policy

## Supported versions

mypackage is pre-1.0 and follows a "latest minor" support model: security fixes
are applied to the most recent released minor version. We recommend always
running the latest release.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, use GitHub's private vulnerability reporting:

1. Go to the repository's **Security** tab.
2. Click **Report a vulnerability** to open a private advisory.

This delivers your report directly to the maintainers without disclosing it
publicly. If private reporting is unavailable to you, open a minimal public issue
asking a maintainer to contact you privately — do **not** include exploit details
there.

Please include, as available:

- A description of the vulnerability and its impact.
- Steps to reproduce or a proof of concept.
- Affected version(s) and environment (OS, Python version).

### Response commitment

- **Acknowledgement:** within 3 business days.
- **Initial assessment:** within 10 business days.
- **Fix & disclosure:** we aim to release a patch and publish an advisory within
  30 days of confirmation, coordinating the disclosure timeline with the
  reporter.

We will credit reporters in the advisory unless you ask to remain anonymous.

## Security-relevant design notes

<!-- Replace this section with the specifics of your project. Be concrete about
     what crosses a trust boundary: network calls, deserialization, subprocess
     execution, credentials, and any code paths that execute user input. -->

- **No network access.** mypackage performs no outbound requests.
- **Untrusted input.** Functions registered through `register()` execute as
  ordinary Python. Do not register callables built from untrusted input.
