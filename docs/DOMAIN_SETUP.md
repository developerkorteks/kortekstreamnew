# Domain Setup Guide - kortekstream.online

Complete guide for setting up KortekStream on domain kortekstream.online

## Domain Configuration

**Domain**: kortekstream.online
**Subdomains**: www.kortekstream.online

## 1. Environment Configuration

### Production Environment File

Use `.env.production` as template for production:

```env
# Django Core
DEBUG=False
SECRET_KEY=your-secure-random-string-min-50-characters

# Domain Configuration
ALLOWED_HOSTS=kortekstream.online,www.kortekstream.online

# CSRF Protection
CSRF_TRUSTED_ORIGINS=https://kortekstream.online,https://www.kortekstream.online,http://kortekstream.online,http://www.kortekstream.online

# API Configuration
STREAMEX_API_BASE_URL=http://localhost:5000/api
API_TIMEOUT=30

# Security (Auto-enabled when DEBUG=False)
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Generate Secure SECRET_KEY

```python
# Run in Python shell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it as SECRET_KEY in .env

## 2. DNS Configuration

Point your domain to your server:

### A Records
```
Type    Name    Value           TTL
A       @       YOUR_SERVER_IP  3600
A       www     YOUR_SERVER_IP  3600
```

### Verify DNS
```bash
# Check DNS propagation
dig kortekstream.online
dig www.kortekstream.online

# Or
nslookup kortekstream.online
nslookup www.kortekstream.online
```

## 3. Nginx Configuration

### SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Get certificate for both domains
sudo certbot --nginx -d kortekstream.online -d www.kortekstream.online

# Auto-renewal (test)
sudo certbot renew --dry-run
```

### Nginx Config

File: `/etc/nginx/sites-available/kortekstream`

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name kortekstream.online www.kortekstream.online;
    
    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    # Redirect all HTTP to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name kortekstream.online www.kortekstream.online;

    # SSL Configuration (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/kortekstream.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kortekstream.online/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Static Files (served by Nginx for better performance)
    location /static/ {
        alias /path/to/kortekstream/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Media Files (if any)
    location /media/ {
        alias /path/to/kortekstream/media/;
        expires 30d;
        access_log off;
    }

    # Proxy to PM2/Gunicorn
    location / {
        proxy_pass http://127.0.0.1:63847;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 24 4k;
        proxy_busy_buffers_size 8k;
        proxy_max_temp_file_size 2048m;
        proxy_temp_file_write_size 32k;
    }

    # Logging
    access_log /var/log/nginx/kortekstream-access.log;
    error_log /var/log/nginx/kortekstream-error.log;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss image/svg+xml;
}
```

### Enable Site

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/kortekstream /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## 4. CSRF Configuration

### How CSRF Protection Works

Django's CSRF protection requires:
1. **ALLOWED_HOSTS**: Validates Host header
2. **CSRF_TRUSTED_ORIGINS**: Validates Origin/Referer headers

### Configuration in settings.py

Already configured:
```python
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost:8000,http://127.0.0.1:8000'
).split(',')
```

### Required in .env

```env
ALLOWED_HOSTS=kortekstream.online,www.kortekstream.online

CSRF_TRUSTED_ORIGINS=https://kortekstream.online,https://www.kortekstream.online,http://kortekstream.online,http://www.kortekstream.online
```

**Important**: Include both HTTP and HTTPS protocols!

## 5. Deployment Steps

### Step 1: Update .env

```bash
# Copy production template
cp .env.production .env

# Edit with your values
nano .env
```

Set:
- DEBUG=False
- SECRET_KEY=your-secure-key
- ALLOWED_HOSTS=kortekstream.online,www.kortekstream.online
- CSRF_TRUSTED_ORIGINS with both HTTP and HTTPS

### Step 2: Build & Deploy

```bash
# Build CSS
npm run build:css

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start with PM2
npm run pm2:start
```

### Step 3: Test

```bash
# Check PM2 status
npm run pm2:status

# Check logs
npm run pm2:logs

# Test locally first
curl http://localhost:63847

# Test domain (after DNS propagation)
curl https://kortekstream.online
```

## 6. Security Checklist

- [ ] DEBUG=False in production .env
- [ ] Strong SECRET_KEY (50+ characters)
- [ ] ALLOWED_HOSTS set to your domain only
- [ ] CSRF_TRUSTED_ORIGINS includes HTTPS
- [ ] SSL certificate installed (Let's Encrypt)
- [ ] Nginx configured with security headers
- [ ] HSTS enabled (SECURE_HSTS_SECONDS=31536000)
- [ ] All security settings in .env
- [ ] Firewall configured (only ports 80, 443, 22)
- [ ] Regular backups configured

## 7. Testing CSRF Protection

### Test Valid Request (Should Work)

```bash
# From browser console on kortekstream.online
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({data: 'test'})
})
```

### Test Invalid Origin (Should Fail)

```bash
# From different domain
curl -X POST https://kortekstream.online/api/endpoint/ \
  -H "Origin: https://evil.com" \
  -H "Content-Type: application/json"

# Expected: 403 Forbidden
```

## 8. Troubleshooting

### CSRF Verification Failed

**Error**: "CSRF verification failed. Request aborted."

**Solutions**:

1. Check CSRF_TRUSTED_ORIGINS in .env:
   ```env
   CSRF_TRUSTED_ORIGINS=https://kortekstream.online,https://www.kortekstream.online
   ```

2. Include protocol (https://)
3. No trailing slashes
4. Restart application:
   ```bash
   npm run pm2:restart
   ```

### Invalid HTTP_HOST Header

**Error**: "Invalid HTTP_HOST header: 'kortekstream.online'"

**Solutions**:

1. Check ALLOWED_HOSTS in .env:
   ```env
   ALLOWED_HOSTS=kortekstream.online,www.kortekstream.online
   ```

2. No spaces in comma-separated list
3. Include both www and non-www
4. Restart application

### SSL Redirect Loop

**Issue**: Infinite redirect loop

**Solution**:

Add to Nginx config:
```nginx
proxy_set_header X-Forwarded-Proto $scheme;
```

And in Django settings (already configured):
```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

## 9. Monitoring

### Check Application

```bash
# PM2 status
npm run pm2:status

# Logs
npm run pm2:logs

# Monitor
npm run pm2:monit
```

### Check Nginx

```bash
# Access logs
sudo tail -f /var/log/nginx/kortekstream-access.log

# Error logs
sudo tail -f /var/log/nginx/kortekstream-error.log

# Test config
sudo nginx -t
```

### Check SSL

```bash
# SSL certificate info
sudo certbot certificates

# Test SSL (external tool)
# https://www.ssllabs.com/ssltest/analyze.html?d=kortekstream.online
```

## 10. Maintenance

### Update SSL Certificate

Certbot auto-renews, but to manually renew:
```bash
sudo certbot renew
sudo systemctl reload nginx
```

### Update Application

```bash
git pull
npm install
pip install -r requirements.txt
npm run build:css
python manage.py migrate
python manage.py collectstatic --noinput
npm run pm2:restart
```

### Backup

```bash
# Database
cp db.sqlite3 backups/db.sqlite3.$(date +%Y%m%d)

# Media (if any)
tar -czf backups/media-$(date +%Y%m%d).tar.gz media/

# .env file
cp .env backups/.env.$(date +%Y%m%d)
```

## Summary

**Domain**: kortekstream.online, www.kortekstream.online
**HTTPS**: Required (Let's Encrypt)
**Port**: 63847 (internal, proxied by Nginx)
**CSRF**: Configured for your domain
**Security**: HSTS, SSL redirect, secure cookies

Your application is ready for production at https://kortekstream.online! 🚀
