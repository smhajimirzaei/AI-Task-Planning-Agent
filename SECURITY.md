# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **DO NOT** open a public issue
2. Email the maintainer directly (or use GitHub's private vulnerability reporting)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to resolve the issue.

## Security Best Practices

When using this project:

### API Keys
- **Never commit** API keys to version control
- Store keys in `.env` file (which is gitignored)
- Rotate keys regularly
- Use environment-specific keys (dev vs prod)

### Calendar Credentials
- Keep `credentials.json` and `token.json` secure
- Never share these files
- Ensure proper OAuth scopes (minimal required permissions)
- Use separate calendars for testing

### Database
- Protect database file permissions
- Regular backups recommended
- Consider encryption for sensitive data
- Use connection pooling for production

### Dependencies
- Keep dependencies updated
- Monitor for security advisories
- Use virtual environments
- Review dependency licenses

## Known Limitations

- API keys stored in environment variables (consider using secret management in production)
- SQLite is suitable for single-user; use PostgreSQL for multi-user
- No built-in authentication/authorization (add if exposing as web service)

## Updates

We recommend:
- Star/watch this repository for security updates
- Check CHANGELOG.md regularly
- Update dependencies monthly
- Test updates in development before production

Thank you for helping keep this project secure!
