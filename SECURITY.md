# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 3.0.x   | :white_check_mark: |
| < 3.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in ImageGhost, please report it responsibly.

### Reporting Process

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security issues via:

1. **GitHub Security Advisories** (Preferred):
   - Go to: https://github.com/yourusername/ImageGhost/security/advisories
   - Click "Report a vulnerability"
   - Fill in the vulnerability details

2. **Email** (Alternative):
   - Email: security@yourdomain.com
   - Subject: [SECURITY] ImageGhost Vulnerability Report
   - Include: Detailed description, reproduction steps, impact assessment

### What to Include

Please include the following information:
- Type of vulnerability
- Affected component(s)
- Steps to reproduce
- Potential impact
- Suggested fix (if available)
- Your name/handle for credit (if you want attribution)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Triage & Assessment**: Within 5 business days
- **Fix Development**: Depends on severity (Critical: 1-7 days, High: 7-14 days, Medium: 14-30 days)
- **Public Disclosure**: After fix is released or 90 days, whichever comes first

### Security Considerations

ImageGhost is designed with security in mind:

- **No External Connections**: All processing is local-only
- **Cryptographically Secure Random**: Uses Python's `secrets` module
- **Memory Clearing**: Sensitive data cleared after operations
- **Authenticated Encryption**: AES-256-GCM with AEAD
- **Strong Key Derivation**: Argon2id with hardened parameters
- **Secure Deletion**: Multiple overwrite passes (DoD 5220.22-M, Gutmann)
- **Open Source**: Full code transparency for auditing

### Out of Scope

The following are generally considered out of scope:
- Issues in third-party dependencies (report to upstream)
- Social engineering attacks
- Physical access attacks
- Theoretical attacks without practical exploitation
- Issues requiring user to run malicious code

### Responsible Disclosure

We follow coordinated vulnerability disclosure:
1. Report received and acknowledged
2. Issue verified and assessed
3. Fix developed and tested
4. Security advisory drafted
5. Fix released with version update
6. Public disclosure with credit to reporter

### Security Best Practices for Users

1. **Always verify downloads**: Check file hashes and signatures
2. **Keep updated**: Use the latest version
3. **Strong passwords**: Use cryptographically secure passwords
4. **Secure storage**: Store encrypted files securely
5. **Verify deletion**: Confirm original files are shredded
6. **Offline usage**: Run on air-gapped systems for maximum security

### Security Hall of Fame

We acknowledge security researchers who help us improve ImageGhost:

- (Be the first to responsibly disclose a vulnerability!)

### Legal

This security policy is in addition to our MIT License. We encourage responsible disclosure and will not pursue legal action against researchers who follow this policy.

---

**Thank you for helping keep ImageGhost secure!**

Last Updated: 2026-03-25
