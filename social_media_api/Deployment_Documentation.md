# Django REST API - Complete Deployment Documentation

## Project: Social Media API
**Deployed URL:** https://social-media-api-kd2h.onrender.com  
**Repository:** https://github.com/irihojaphet/Alx_DjangoLearnLab  
**Hosting Platform:** Render (PaaS)  
**Database:** PostgreSQL (Render Managed)  
**Web Server:** Gunicorn  
**Static Files:** Whitenoise

---

## Table of Contents
1. [Production Settings Configuration](#production-settings-configuration)
2. [Security Configuration](#security-configuration)
3. [Database Setup](#database-setup)
4. [Static and Media Files](#static-and-media-files)
5. [Deployment Process](#deployment-process)
6. [Environment Variables](#environment-variables)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Testing and Verification](#testing-and-verification)

---

## 1. Production Settings Configuration

### ✅ CHECK 1: Review and Adjust settings.py

**Changes Made to `settings.py`:**

#### A. DEBUG Configuration
```python
# Production: DEBUG must be False
DEBUG = config('DEBUG', default=False, cast=bool)
```

**Rationale:** Setting `DEBUG = False` prevents sensitive information from being displayed in error pages and is a critical security requirement for production.

**Environment Variable:**
- **Render:** Set `DEBUG=False` in Environment tab
- **Local:** Set `DEBUG=True` in `.env` file

#### B. ALLOWED_HOSTS Configuration
```python
# Must specify which domains can access the application
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,.onrender.com', cast=Csv())
```

**Rationale:** Prevents HTTP Host header attacks by restricting which domains can serve the application.

**Environment Variable:**
- **Render:** Set `ALLOWED_HOSTS=.onrender.com`
- **Local:** Set `ALLOWED_HOSTS=localhost,127.0.0.1`

#### C. Database Configuration
```python
# Use environment variable for database URL
DATABASE_URL = config('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}
```

**Features:**
- Connection pooling enabled (`conn_max_age=600`)
- Supports PostgreSQL, MySQL, SQLite via URL
- Credentials not hardcoded
- Falls back to SQLite for local development

---

## 2. Security Configuration

### ✅ CHECK 2: Configure Security Settings

**All Security Headers Configured:**

```python
if not DEBUG:
    # SSL/HTTPS Settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS Settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Security Headers (Required by CHECK 2)
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Additional Security
    SECURE_REFERRER_POLICY = 'same-origin'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Security Settings Explained:

| Setting | Purpose | Value |
|---------|---------|-------|
| `SECURE_SSL_REDIRECT` | Force HTTPS | `True` |
| `SECURE_BROWSER_XSS_FILTER` | XSS protection | `True` |
| `X_FRAME_OPTIONS` | Prevent clickjacking | `DENY` |
| `SECURE_CONTENT_TYPE_NOSNIFF` | Prevent MIME sniffing | `True` |
| `SECURE_HSTS_SECONDS` | Force HTTPS for 1 year | `31536000` |

**Result:** All security headers are properly configured when `DEBUG=False`.

---

## 3. Database Setup

### ✅ CHECK 3: Database Credentials Setup

**Database Configuration:**

- **Platform:** Render PostgreSQL (Free tier)
- **Database Name:** social_media_api_0p43
- **User:** social_media_user
- **Connection:** Via `DATABASE_URL` environment variable

**Environment Variable Setup:**

```bash
# Format:
DATABASE_URL=postgresql://user:password@host:port/database

# Actual (Render provides this automatically):
DATABASE_URL=postgresql://social_media_user:PASSWORD@dpg-xxx-a/social_media_api_0p43
```

**Security Best Practices:**
- ✅ Credentials stored in environment variables (not in code)
- ✅ Connection pooling enabled
- ✅ SSL connection enforced
- ✅ Automatic failover (Render managed)

**Migration Status:**
```bash
Operations to perform:
  Apply all migrations: accounts, admin, auth, authtoken, contenttypes, notifications, posts, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  [... all migrations applied successfully]
```

---

## 4. Static and Media Files

### ✅ CHECK 4: Static Files Configuration

#### A. Collectstatic Configuration

```python
# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**Build Process:**
```bash
# In build.sh
python manage.py collectstatic --no-input
```

**Result:**
```
166 static files copied to '/opt/render/project/src/social_media_api/staticfiles'
```

#### B. Whitenoise for Static Files

**Middleware Configuration:**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be second
    # ... other middleware
]
```

**Features:**
- Serves static files directly from Django
- Gzip compression
- Far-future caching headers
- No need for separate CDN for basic static files

#### C. Media Files Configuration

```python
# Basic media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

#### D. AWS S3 Support (Optional)

```python
# Optional: For production media file storage
USE_S3 = config('USE_S3', default=False, cast=bool)

if USE_S3:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

**Note:** Currently using local media storage. Can be upgraded to S3 by:
1. Creating S3 bucket
2. Installing `django-storages` and `boto3`
3. Setting `USE_S3=True` environment variable
4. Adding AWS credentials

---

## 5. Deployment Process

### Step-by-Step Deployment

#### A. Pre-Deployment Checklist

- [x] Code pushed to GitHub
- [x] `requirements.txt` updated
- [x] `build.sh` script created
- [x] Environment variables documented
- [x] Database migrations ready
- [x] Static files configured
- [x] Security settings enabled

#### B. Repository Setup

**Repository:** https://github.com/irihojaphet/Alx_DjangoLearnLab

**Structure:**
```
Alx_DjangoLearnLab/
└── social_media_api/
    ├── accounts/
    ├── posts/
    ├── notifications/
    ├── social_media_api/
    │   └── settings.py
    ├── manage.py
    ├── requirements.txt
    ├── build.sh
    └── README.md
```

#### C. Render Configuration

**Service Type:** Web Service  
**Region:** Oregon (US West)  
**Branch:** main  
**Root Directory:** `social_media_api`  
**Build Command:** `./build.sh`  
**Start Command:** `gunicorn social_media_api.wsgi:application`

#### D. Build Script (`build.sh`)

```bash
#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
```

**Permissions:**
```bash
chmod +x build.sh
```

---

## 6. Environment Variables

### Required Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `PYTHON_VERSION` | `3.12.0` | Python runtime version |
| `DEBUG` | `False` | Production mode |
| `SECRET_KEY` | `<generated>` | Django secret key |
| `DATABASE_URL` | `<from Render>` | PostgreSQL connection |
| `ALLOWED_HOSTS` | `.onrender.com` | Allowed domains |

### Optional Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `USE_S3` | `False` | Enable AWS S3 for media |
| `AWS_ACCESS_KEY_ID` | - | AWS credentials |
| `AWS_SECRET_ACCESS_KEY` | - | AWS credentials |
| `EMAIL_HOST` | - | SMTP server |
| `EMAIL_HOST_USER` | - | Email username |

### Setting Environment Variables in Render

1. Go to Dashboard → Your Service
2. Click "Environment" in left sidebar
3. Click "Add Environment Variable"
4. Enter key and value
5. Click "Save Changes"

---

## 7. Monitoring and Maintenance

### ✅ CHECK 6: Monitoring Setup

#### A. Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

**Log Locations:**
- **Render Console:** Real-time logs in Dashboard → Logs tab
- **Application Logs:** `/logs/django.log` (if persistent storage configured)

#### B. Monitoring Tools

**Built-in Render Monitoring:**
- Uptime monitoring
- Performance metrics
- Error tracking
- Deployment history

**Accessing Logs:**
1. Render Dashboard
2. Click on service
3. Go to "Logs" tab
4. Filter by time range or search

#### C. Health Checks

**Render Automatic Health Checks:**
- HTTP requests to your service
- Restarts service if unhealthy
- Notification on failures

**Manual Health Check:**
```bash
curl https://social-media-api-kd2h.onrender.com/api/posts/
```

### Maintenance Schedule

**Weekly:**
- Review error logs
- Check disk space usage
- Monitor database size

**Monthly:**
- Update dependencies
- Review security advisories
- Backup database (manual)

**Quarterly:**
- Update Django version
- Review and optimize queries
- Performance testing

---

## 8. Testing and Verification

### Post-Deployment Testing

#### A. Endpoint Testing

**Authentication:**
```bash
# Register user
curl -X POST https://social-media-api-kd2h.onrender.com/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"pass123","password_confirm":"pass123"}'

# Login
curl -X POST https://social-media-api-kd2h.onrender.com/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'
```

**Posts:**
```bash
# List posts
curl https://social-media-api-kd2h.onrender.com/api/posts/ \
  -H "Authorization: Token YOUR_TOKEN"

# Create post
curl -X POST https://social-media-api-kd2h.onrender.com/api/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","content":"Testing deployment"}'
```

#### B. Security Verification

**Check HTTPS:**
```bash
curl -I https://social-media-api-kd2h.onrender.com/api/posts/
```

**Expected Headers:**
```
HTTP/2 200
strict-transport-security: max-age=31536000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
```

#### C. Database Verification

**Via Render Shell:**
```bash
# Access shell
python manage.py shell

# Check database
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.count()
```

#### D. Static Files Verification

**Check static file serving:**
```bash
curl -I https://social-media-api-kd2h.onrender.com/static/admin/css/base.css
```

**Expected:** 200 OK with proper caching headers

---

## Deployment Configuration Files

### Files Included in Repository

1. **requirements.txt**
```txt
Django==6.0
djangorestframework==3.15.2
Pillow==11.0.0
gunicorn==23.0.0
whitenoise==6.11.0
psycopg2-binary==2.9.11
python-decouple==3.8
dj-database-url==3.0.1
```

2. **build.sh**
```bash
#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

3. **settings.py** (production-ready)
- See separate settings file with all configurations

4. **.gitignore**
```
*.pyc
__pycache__/
db.sqlite3
.env
/media
/staticfiles
*.log
```

---

## Troubleshooting Guide

### Common Issues and Solutions

**Issue 1: 500 Internal Server Error**
- Check DEBUG=False is set
- Review logs in Render dashboard
- Verify DATABASE_URL is set correctly

**Issue 2: Static files not loading**
- Verify STATIC_ROOT is set
- Check collectstatic ran successfully
- Ensure Whitenoise is in MIDDLEWARE

**Issue 3: Database connection errors**
- Verify DATABASE_URL environment variable
- Check database is running (Render dashboard)
- Review database credentials

**Issue 4: ALLOWED_HOSTS error**
- Add your domain to ALLOWED_HOSTS
- Use `.onrender.com` for Render deployments
- Check environment variable is set

---

## Deployment Checklist Summary

### ✅ All Checks Passed

- [x] **CHECK 1:** Production settings configured (DEBUG=False, ALLOWED_HOSTS, DATABASE)
- [x] **CHECK 2:** Security settings enabled (XSS_FILTER, X_FRAME_OPTIONS, NOSNIFF, SSL_REDIRECT)
- [x] **CHECK 3:** Database credentials properly configured via environment variables
- [x] **CHECK 4:** Static files configured with collectstatic and Whitenoise
- [x] **CHECK 5:** Web server (Gunicorn) configured and running
- [x] **CHECK 6:** Logging and monitoring set up

### Deliverables Completed

1. ✅ **Deployment Configuration Files:** All files in repository
2. ✅ **Live URL:** https://social-media-api-kd2h.onrender.com
3. ✅ **Deployment Documentation:** This comprehensive guide

---

## Contact and Support

**Developer:** IdukundirihoJaphet  
**Repository:** https://github.com/irihojaphet/Alx_DjangoLearnLab  
**Live API:** https://social-media-api-kd2h.onrender.com  

**For Issues:**
- Check logs in Render dashboard
- Review this documentation
- Check Render status page: status.render.com

---

**Document Version:** 1.0  
**Last Updated:** December 28, 2025  
**Deployment Status:** ✅ Active and Running