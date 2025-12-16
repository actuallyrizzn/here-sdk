# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public issue. Instead, please report it privately:

1. **Email**: [security@example.com] (replace with actual security contact)
2. **Subject**: "Security Vulnerability in HERE Traffic SDK"

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

We will:
- Acknowledge receipt within 48 hours
- Provide an initial assessment within 7 days
- Keep you informed of our progress
- Credit you in the security advisory (if you wish)

## Security Best Practices

### API Key Security
- **Never commit API keys to version control**
- Use environment variables or secure credential stores
- Rotate API keys regularly
- Restrict API keys to trusted domains when possible

### OAuth Credentials
- Store credentials securely
- Never expose credentials in client-side code
- Use token refresh mechanisms
- Rotate credentials periodically

### General Security
- Keep dependencies up to date
- Use HTTPS for all API requests
- Implement rate limiting on your side
- Monitor API usage for anomalies
- Review and audit API access regularly

## Disclosure Policy

When we receive a security bug report, we will:
1. Confirm the issue and determine affected versions
2. Develop a fix
3. Release the fix in a timely manner
4. Publicly disclose the vulnerability after the fix is available

We follow responsible disclosure practices and will credit researchers who report vulnerabilities responsibly.

