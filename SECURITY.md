# Security Policy

## Supported Versions

The following versions of `indianconstitution` are actively supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| v1.3.x  | ✅ Active support  |
| v1.2.x  | ✅ Active support  |
| v1.1.x  | ⚠️ Critical only   |
| < v1.1  | ❌ End of life     |

## Reporting a Vulnerability

We take supply-chain and data integrity security seriously. If you believe you have found a security vulnerability, **do not open a public GitHub issue**. Instead, follow the responsible disclosure process below:

### Preferred Method: GitHub Security Advisory

1. Navigate to [Security Advisories](https://github.com/Vikhram-S/IndianConstitution/security/advisories/new)
2. Click **"New draft security advisory"**
3. Provide a clear description, steps to reproduce, potential impact, and any suggested mitigations

### Alternative: Email

Send a detailed report to **vikhrams@saveetha.ac.in** with:
- **Subject**: `[SECURITY] IndianConstitution — <brief description>`
- Steps to reproduce
- Potential impact assessment
- Any suggested fixes or patches

### Response Timeline

| Stage | Timeline |
|:---|:---|
| Acknowledgement | Within 48 hours |
| Severity assessment | Within 72 hours |
| Fix / workaround | Within 14 days (critical), 30 days (moderate) |
| Public disclosure | After fix is released and users notified |

## Supply-Chain Security

This package implements OSSF Scorecard recommendations:
- All GitHub Actions are pinned to **immutable SHA hashes** (no floating `@main` or `@latest`)
- **Dependabot** is configured for automated dependency update PRs
- **CodeQL** static analysis runs on every push to `main`
- Releases are published via **OIDC Trusted Publishing** (no long-lived PyPI tokens)

Thank you for helping keep `indianconstitution` and its users secure!
