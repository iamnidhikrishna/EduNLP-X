# Security Updates - EduNLP-X

## Overview

This document tracks security vulnerability fixes applied to the EduNLP-X project dependencies based on security audit recommendations.

## Updated Dependencies

### Backend (backend/requirements.txt)

| Package | Previous Version | Updated Version | Vulnerabilities Fixed |
|---------|------------------|-----------------|----------------------|
| **python-jose** | 3.3.0 | **3.4.0** | CVE-2024-33663 (CRITICAL), CVE-2024-33664 (MEDIUM) |
| **python-multipart** | 0.0.6 | **0.0.18** | CVE-2024-24762 (HIGH), CVE-2024-53981 (HIGH) |
| **langchain** | 0.1.0 | **0.2.5** | CVE-2024-2965 (MEDIUM), CVE-2024-8309 (LOW) |
| **langchain-community** | 0.0.10 | **0.2.9** | CVE-2024-5998 (HIGH), CVE-2025-2828 (HIGH), CVE-2024-2965 (MEDIUM), CVE-2024-3095 (MEDIUM) |
| **langchain-openai** | 0.0.5 | **0.1.3** | Compatibility update with langchain 0.2.5 |
| **pypdf2** | 3.0.1 | **pypdf 4.0.1** | CVE-2023-36464 (MEDIUM), replaced with pypdf |
| **pillow** | 10.1.0 | **10.3.0** | CVE-2023-50447 (CRITICAL), CVE-2024-28219 (HIGH) |
| **black** | 23.12.1 | **24.3.0** | CVE-2024-21503 (MEDIUM) |

### Streamlit App (streamlit_app/requirements.txt)

| Package | Previous Version | Updated Version | Vulnerabilities Fixed |
|---------|------------------|-----------------|----------------------|
| **streamlit** | 1.29.0 | **1.37.0** | CVE-2024-42474 (MEDIUM), GHSA-8qw9-gf7w-42x5 (LOW) |
| **requests** | 2.31.0 | **2.32.4** | CVE-2024-35195 (MEDIUM), CVE-2024-47081 (MEDIUM) |

## Vulnerability Details

### Critical Severity

1. **CVE-2024-33663** - python-jose: Algorithm confusion with OpenSSH ECDSA keys and other key formats
   - **Impact**: Critical security flaw in JWT token handling
   - **Fix**: Updated to python-jose 3.4.0

2. **CVE-2023-50447** - pillow: Arbitrary Code Execution via the environment parameter
   - **Impact**: Potential arbitrary code execution
   - **Fix**: Updated to pillow 10.3.0

### High Severity

3. **CVE-2024-24762** - python-multipart: DoS vulnerability in multipart parsing
   - **Impact**: Denial of Service attacks
   - **Fix**: Updated to python-multipart 0.0.18

4. **CVE-2024-53981** - python-multipart: DoS via deformed multipart/form-data boundary
   - **Impact**: Denial of Service attacks
   - **Fix**: Updated to python-multipart 0.0.18

5. **CVE-2024-5998** - LangChain: Pickle deserialization of untrusted data
   - **Impact**: Potential remote code execution
   - **Fix**: Updated to langchain-community 0.2.9

6. **CVE-2025-2828** - langchain-community: SSRF Vulnerability
   - **Impact**: Server-Side Request Forgery attacks
   - **Fix**: Updated to langchain-community 0.2.9

7. **CVE-2024-28219** - pillow: Buffer overflow in _imagingcms.c
   - **Impact**: Potential buffer overflow
   - **Fix**: Updated to pillow 10.3.0

### Medium Severity

8. **CVE-2024-33664** - python-jose: DoS vulnerability
   - **Fix**: Updated to python-jose 3.4.0

9. **CVE-2024-2965** - langchain-community: SitemapParser DoS Vulnerability
   - **Fix**: Updated to langchain-community 0.2.9

10. **CVE-2024-3095** - langchain-community: SSRF in WebResearchRetriever
    - **Fix**: Updated to langchain-community 0.2.9

11. **CVE-2023-36464** - pypdf2: Possible Infinite Loop in comment parsing
    - **Fix**: Replaced pypdf2 with pypdf 4.0.1

12. **CVE-2024-21503** - black: ReDoS via lines_with_leading_tabs_expanded()
    - **Fix**: Updated to black 24.3.0

13. **CVE-2024-42474** - streamlit: Path traversal vulnerability on Windows
    - **Fix**: Updated to streamlit 1.37.0

14. **CVE-2024-35195** - requests: Certificate verification bypass
    - **Fix**: Updated to requests 2.32.4

15. **CVE-2024-47081** - requests: .netrc credentials leak via malicious URLs
    - **Fix**: Updated to requests 2.32.4

### Low Severity

16. **CVE-2024-8309** - langchain: SQL Injection vulnerability
    - **Fix**: Updated to langchain 0.2.5

17. **GHSA-8qw9-gf7w-42x5** - streamlit: Minor fix to previous patch
    - **Fix**: Updated to streamlit 1.37.0

## Breaking Changes and Compatibility

### LangChain Upgrade (0.1.0 → 0.2.5)

The LangChain upgrade from 0.1.0 to 0.2.5 includes significant API changes:

1. **Import Changes**: Some imports may need to be updated when implementing AI features
2. **API Changes**: Method signatures and class structures may have changed
3. **Compatibility**: langchain-openai updated to 0.1.3 for compatibility

### pypdf2 → pypdf Migration

- **Package Name Change**: `pypdf2` has been replaced with `pypdf`
- **Import Changes**: Any future imports should use `from pypdf import PdfReader` instead of `from PyPDF2 import PdfFileReader`
- **API Changes**: The new pypdf library has a slightly different API

## Testing Required

After these updates, the following should be tested:

1. **Authentication**: JWT token generation and validation
2. **File Upload**: PDF and multipart file upload functionality
3. **AI Features**: LangChain integration when implemented
4. **Image Processing**: Pillow-dependent image processing
5. **Streamlit Interface**: All Streamlit functionality
6. **HTTP Requests**: API calls and external requests

## Development Impact

- All dependency versions have been updated to secure versions
- No immediate code changes required as AI features are not yet implemented
- Future implementation should use the new API versions
- Development environment should be rebuilt with updated dependencies

## Next Steps

1. **Rebuild Environment**: Run `make clean && make setup` to update dependencies
2. **Test Basic Functionality**: Ensure core application still works
3. **Update Documentation**: Any API examples should use new versions
4. **Monitor Dependencies**: Set up automated dependency scanning for future updates

## Security Best Practices

Moving forward:

1. **Regular Updates**: Keep dependencies updated regularly
2. **Automated Scanning**: Use tools like Dependabot or similar
3. **Security Monitoring**: Monitor CVE databases for new vulnerabilities
4. **Staged Updates**: Test updates in development before production
5. **Version Pinning**: Continue to pin exact versions for reproducible builds

---

**Update Date:** August 22, 2024  
**Applied By:** EduNLP-X Development Team  
**Status:** ✅ Complete
