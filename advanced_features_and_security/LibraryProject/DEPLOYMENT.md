# Deployment Configuration Guide

This document provides instructions for deploying the Django application with HTTPS support and secure configuration.

## Overview

This guide covers:
- SSL/TLS certificate setup
- Web server configuration (Nginx and Apache)
- Django settings for production
- Environment variable configuration
- HTTPS enforcement setup

## Prerequisites

- Django application ready for deployment
- Domain name configured
- SSH access to production server
- Root or sudo access on server
- Basic knowledge of Linux command line

## SSL/TLS Certificate Setup

### Option 1: Let's Encrypt (Free, Recommended)

Let's Encrypt provides free SSL certificates that are automatically renewed.

#### Installation

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx  # For Nginx
# OR
sudo apt-get install certbot python3-certbot-apache  # For Apache
```

#### Obtain Certificate

```bash
# For Nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# For Apache
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com

# Standalone (if not using Nginx/Apache)
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

#### Auto-renewal

Certbot sets up automatic renewal. Test it with:

```bash
sudo certbot renew --dry-run
```

Certificates are stored at:
- `/etc/letsencrypt/live/yourdomain.com/fullchain.pem` (certificate)
- `/etc/letsencrypt/live/yourdomain.com/privkey.pem` (private key)

### Option 2: Commercial SSL Certificate

If using a commercial SSL certificate provider:

1. Purchase SSL certificate from provider
2. Generate Certificate Signing Request (CSR)
3. Complete domain validation
4. Download certificate files
5. Install certificate on server

## Nginx Configuration

### Basic Nginx Configuration with HTTPS

Create or edit `/etc/nginx/sites-available/libraryproject`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect all HTTP traffic to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS server configuration
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Configuration for Security
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Maximum upload size
    client_max_body_size 75M;
    
    # Static files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /path/to/your/project/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_redirect off;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Enable Site

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/libraryproject /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## Apache Configuration

### Basic Apache Configuration with HTTPS

Create or edit `/etc/apache2/sites-available/libraryproject.conf`:

```apache
# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # Redirect all HTTP traffic to HTTPS
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS server configuration
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL Certificate Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    
    # SSL Configuration for Security
    SSLProtocol all -SSLv2 -SSLv3
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off
    SSLSessionTickets off
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    
    # Proxy settings
    ProxyPreserveHost On
    ProxyPass /static/ !
    ProxyPass /media/ !
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    
    # Static files
    Alias /static/ /path/to/your/project/staticfiles/
    <Directory /path/to/your/project/staticfiles/>
        Require all granted
    </Directory>
    
    # Media files
    Alias /media/ /path/to/your/project/media/
    <Directory /path/to/your/project/media/>
        Require all granted
    </Directory>
    
    # WSGI configuration
    WSGIDaemonProcess libraryproject python-home=/path/to/venv python-path=/path/to/project
    WSGIProcessGroup libraryproject
    WSGIScriptAlias / /path/to/project/LibraryProject/wsgi.py
    
    <Directory /path/to/project/LibraryProject>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

### Enable Required Modules

```bash
# Enable required Apache modules
sudo a2enmod ssl
sudo a2enmod headers
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod rewrite

# Enable site
sudo a2ensite libraryproject.conf

# Test configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2
```

## Django Settings Configuration

### Environment Variables

Create a `.env` file or set environment variables on your production server:

```bash
# Security Settings
export DEBUG=False
export SECRET_KEY='your-secure-secret-key-here-generate-with-openssl-rand-hex-32'
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'

# HTTPS Settings
export SECURE_SSL_REDIRECT=True
export SECURE_HSTS_SECONDS=31536000
export SECURE_HSTS_INCLUDE_SUBDOMAINS=True
export SECURE_HSTS_PRELOAD=True

# Secure Cookies
export CSRF_COOKIE_SECURE=True
export SESSION_COOKIE_SECURE=True

# Database (if using PostgreSQL/MySQL)
export DB_NAME=libraryproject_db
export DB_USER=libraryproject_user
export DB_PASSWORD=your-secure-password
export DB_HOST=localhost
export DB_PORT=5432
```

### Production Settings File (Optional)

Create `settings_production.py` that imports from `settings.py`:

```python
# settings_production.py
from .settings import *
import os

# Override settings for production
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure Cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## Systemd Service Configuration

Create `/etc/systemd/system/libraryproject.service`:

```ini
[Unit]
Description=LibraryProject Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/LibraryProject
Environment="PATH=/path/to/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=LibraryProject.settings"
ExecStart=/path/to/venv/bin/gunicorn LibraryProject.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log

[Install]
WantedBy=multi-user.target
```

### Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable libraryproject

# Start service
sudo systemctl start libraryproject

# Check status
sudo systemctl status libraryproject
```

## Static Files Collection

```bash
# Collect static files
python manage.py collectstatic --noinput

# Ensure static files directory exists
mkdir -p /path/to/project/staticfiles
```

## Database Migrations

```bash
# Run migrations
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser
```

## Security Checklist

Before going live, verify:

- [ ] SSL certificate is valid and properly installed
- [ ] All HTTP traffic redirects to HTTPS
- [ ] SECURE_SSL_REDIRECT is set to True
- [ ] SECURE_HSTS_SECONDS is set appropriately
- [ ] CSRF_COOKIE_SECURE is set to True
- [ ] SESSION_COOKIE_SECURE is set to True
- [ ] DEBUG is set to False
- [ ] ALLOWED_HOSTS includes your domain
- [ ] SECRET_KEY is secure and not hardcoded
- [ ] Database credentials are secure
- [ ] Static files are being served correctly
- [ ] Media files are being served correctly
- [ ] Web server logs are configured
- [ ] Firewall rules are configured
- [ ] Regular backups are set up

## Testing HTTPS Configuration

### Test SSL Configuration

```bash
# Test SSL certificate
openssl s_client -connect yourdomain.com:443 -showcerts

# Test with SSL Labs (online)
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com
```

### Test Security Headers

```bash
# Test HSTS header
curl -I https://yourdomain.com | grep -i strict-transport-security

# Test X-Frame-Options
curl -I https://yourdomain.com | grep -i x-frame-options

# Test all headers
curl -I https://yourdomain.com
```

### Test HTTPS Redirect

```bash
# Should redirect to HTTPS
curl -I http://yourdomain.com

# Should return 301 or 302 redirect
```

## Monitoring and Maintenance

### Log Monitoring

```bash
# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Django logs
sudo tail -f /var/log/gunicorn/error.log
```

### Certificate Renewal

Let's Encrypt certificates expire every 90 days. Auto-renewal should handle this:

```bash
# Manual renewal
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

### Backup Strategy

1. Database backups (daily)
2. Media files backups (daily)
3. Static files (version controlled)
4. SSL certificates (automatically managed)

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**: Check if Django application is running
2. **SSL Certificate Errors**: Verify certificate paths and permissions
3. **Mixed Content Warnings**: Ensure all resources use HTTPS
4. **HSTS Errors**: Clear browser cache or use incognito mode
5. **Cookie Issues**: Verify SECURE_COOKIE settings match HTTPS status

### Debug Mode

For testing, temporarily enable DEBUG in a separate environment:

```python
# Only for development/testing, never in production
DEBUG = True
ALLOWED_HOSTS = ['*']  # Only for testing
```

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Apache Documentation](https://httpd.apache.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)

