# Security Documentation

This document details the security measures implemented in the Django application to protect against common vulnerabilities.

## Overview

The application implements multiple layers of security to protect against:
- Cross-Site Scripting (XSS) attacks
- Cross-Site Request Forgery (CSRF) attacks
- SQL Injection attacks
- Clickjacking attacks
- MIME type sniffing vulnerabilities

## Security Settings

### 1. DEBUG Mode Configuration

**Location**: `settings.py`

```python
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
```

**Security Measure**: 
- DEBUG is disabled in production using environment variables
- Setting DEBUG=False prevents exposing sensitive error information to users
- Error pages in production don't reveal stack traces or code structure

**Production Setup**:
```bash
export DEBUG=False
```

### 2. XSS Protection Headers

**Location**: `settings.py`

```python
SECURE_BROWSER_XSS_FILTER = True
```

**Security Measure**:
- Enables browser's built-in XSS filtering
- Adds `X-XSS-Protection: 1; mode=block` header to responses
- Provides additional client-side protection against XSS attacks

### 3. Clickjacking Protection

**Location**: `settings.py`

```python
X_FRAME_OPTIONS = 'DENY'
```

**Security Measure**:
- Prevents the site from being displayed in a frame or iframe
- Protects against clickjacking attacks where malicious sites embed your application
- Set to 'DENY' to block all framing attempts

### 4. MIME Type Sniffing Protection

**Location**: `settings.py`

```python
SECURE_CONTENT_TYPE_NOSNIFF = True
```

**Security Measure**:
- Adds `X-Content-Type-Options: nosniff` header
- Prevents browsers from MIME-sniffing response content types
- Protects against MIME type confusion attacks

### 5. Secure Cookies (HTTPS Only)

**Location**: `settings.py`

```python
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False').lower() == 'true'
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
```

**Security Measure**:
- Ensures cookies are only sent over HTTPS connections
- Prevents cookie interception over unencrypted connections
- Must be enabled in production when using HTTPS

**Production Setup**:
```bash
export CSRF_COOKIE_SECURE=True
export SESSION_COOKIE_SECURE=True
```

### 6. HttpOnly Cookies

**Location**: `settings.py`

```python
SESSION_COOKIE_HTTPONLY = True
```

**Security Measure**:
- Prevents JavaScript from accessing session cookies
- Protects against XSS attacks attempting to steal session cookies
- Cookies can only be accessed by the browser, not client-side scripts

### 7. SameSite Cookie Attribute

**Location**: `settings.py`

```python
SESSION_COOKIE_SAMESITE = 'Lax'
```

**Security Measure**:
- Helps protect against CSRF attacks
- 'Lax' allows cookies to be sent with top-level navigations
- Prevents cookies from being sent with cross-site requests in most cases

### 8. HTTPS Redirect

**Location**: `settings.py`

```python
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
```

**Security Measure**:
- Automatically redirects all HTTP requests to HTTPS
- Ensures encrypted communication in production
- Only enable when SSL certificate is properly configured

## CSRF Protection

### Implementation

**Location**: All form templates (`templates/bookshelf/*.html`)

```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

**Security Measure**:
- All forms include `{% csrf_token %}` tag
- Django's `CsrfViewMiddleware` validates CSRF tokens automatically
- Protects against Cross-Site Request Forgery attacks
- Tokens are cryptographically secure and tied to user sessions

### CSRF Middleware

**Location**: `settings.py` → `MIDDLEWARE`

```python
'django.middleware.csrf.CsrfViewMiddleware',
```

This middleware:
- Validates CSRF tokens on all POST requests
- Generates new tokens for forms
- Returns 403 Forbidden for invalid tokens

## SQL Injection Prevention

### Django ORM Usage

**Location**: `bookshelf/views.py`

All database queries use Django ORM, which automatically prevents SQL injection:

```python
# Safe: Django ORM uses parameterized queries
books = Book.objects.all()
book = get_object_or_404(Book, pk=pk)

# Safe: Form save uses parameterized queries
form.save()
```

**Security Measure**:
- Django ORM uses parameterized queries automatically
- User input is never directly inserted into SQL strings
- All field values are properly escaped and validated

### Input Validation

**Location**: `bookshelf/views.py` → `BookForm`

```python
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
```

**Security Measure**:
- Django ModelForm validates all input against model field definitions
- Invalid data is rejected before database operations
- Type conversion and validation happen automatically

## XSS Protection

### Template Escaping

**Location**: All templates (`templates/bookshelf/*.html`)

```html
{{ book.title|escape }}
{{ book.author|escape }}
```

**Security Measure**:
- Django templates automatically escape output by default
- Using `|escape` filter provides explicit escaping
- Prevents malicious scripts from executing in browser
- HTML entities are properly encoded

### Content Security Policy (CSP)

**Location**: `bookshelf/middleware.py` → `CSPMiddleware`

**Settings**: `settings.py`

```python
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:",)
CSP_FONT_SRC = ("'self'",)
```

**Security Measure**:
- CSP headers restrict which domains can load resources
- Prevents unauthorized script execution
- Reduces risk of XSS attacks even if malicious code is injected
- Custom middleware adds CSP headers to all responses

## Permission-Based Access Control

**Location**: `bookshelf/views.py`

All views are protected by authentication and permissions:

```python
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # View implementation
```

**Security Measure**:
- `@login_required` ensures user is authenticated
- `@permission_required` restricts access based on user permissions
- `raise_exception=True` returns 403 Forbidden instead of redirecting
- Prevents unauthorized access to sensitive operations

## Secure Data Access

### Safe Object Retrieval

**Location**: `bookshelf/views.py`

```python
book = get_object_or_404(Book, pk=pk)
```

**Security Measure**:
- `get_object_or_404()` safely handles object retrieval
- Uses parameterized queries (prevents SQL injection)
- Returns 404 for invalid/non-existent objects (prevents information disclosure)
- pk parameter is validated by Django URL routing

### Method Restrictions

**Location**: `bookshelf/views.py`

```python
if request.method == 'POST':
    # Handle form submission
```

**Security Measure**:
- Destructive operations (create, update, delete) require POST method
- Prevents CSRF attacks via GET requests
- Forms use POST with CSRF tokens for all modifications

## Security Testing

### Manual Testing Checklist

1. **CSRF Protection**:
   - [ ] Submit form without CSRF token → Should return 403 Forbidden
   - [ ] Submit form with valid CSRF token → Should work correctly

2. **XSS Protection**:
   - [ ] Try to inject `<script>alert('XSS')</script>` in form fields
   - [ ] Check that output is escaped in rendered HTML
   - [ ] Verify CSP headers are present in responses

3. **SQL Injection**:
   - [ ] Attempt SQL injection in URL parameters (e.g., `pk=1' OR '1'='1`)
   - [ ] Verify that Django ORM handles parameters safely
   - [ ] Check that invalid input returns 404, not SQL errors

4. **Authentication**:
   - [ ] Try to access protected views without logging in → Should redirect to login
   - [ ] Verify permission checks work correctly for different user groups

5. **HTTPS Settings** (Production):
   - [ ] Verify CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE are True
   - [ ] Test that cookies are only sent over HTTPS
   - [ ] Verify SECURE_SSL_REDIRECT redirects HTTP to HTTPS

### Tools for Testing

- **OWASP ZAP**: Automated security testing tool
- **Burp Suite**: Manual security testing and vulnerability scanning
- **Django Debug Toolbar**: For development security checks
- **Browser DevTools**: Check security headers in Network tab

## Production Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with actual domain names
- [ ] Set `SECRET_KEY` from environment variable
- [ ] Enable `CSRF_COOKIE_SECURE=True`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Enable `SECURE_SSL_REDIRECT=True` (if using HTTPS)
- [ ] Configure SSL certificate properly
- [ ] Review and tighten CSP settings
- [ ] Set up proper logging for security events
- [ ] Configure backup and recovery procedures
- [ ] Set up monitoring and alerting

## Environment Variables

Recommended environment variables for production:

```bash
# Security settings
export DEBUG=False
export SECRET_KEY='your-secure-secret-key-here'
export ALLOWED_HOSTS='example.com,www.example.com'
export CSRF_COOKIE_SECURE=True
export SESSION_COOKIE_SECURE=True
export SECURE_SSL_REDIRECT=True
```

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

## Notes

- Some security settings (like `CSRF_COOKIE_SECURE`) are disabled in development for convenience
- Always test security settings in a staging environment before production
- Keep Django and dependencies up to date to receive security patches
- Regularly review and update security configurations based on threat landscape
- Monitor security advisories from Django and other dependencies

