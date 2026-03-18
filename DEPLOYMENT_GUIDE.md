# Deployment Guide - KortekStream

Complete guide for deploying the streaming platform to production.

## Pre-Deployment Checklist

### 1. Environment Configuration

Create/update `.env` file with production settings:

```env
# Django Core Settings
DEBUG=False
SECRET_KEY=your-very-secure-random-key-min-50-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# API Configuration
STREAMEX_API_BASE_URL=https://your-api-url/api
API_TIMEOUT=30

# Optional: Caching
ENABLE_API_CACHE=True
API_CACHE_TTL=3600
```

### 2. Security Settings

The following security settings are recommended for production:

```python
# In settings.py or via environment variables
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 3. Static Files Preparation

```bash
# Build Tailwind CSS for production
npm run build:css

# Collect all static files
python manage.py collectstatic --noinput

# Verify static files
ls -lh staticfiles/
```

### 4. Database

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

## Deployment Steps

### Option 1: Traditional Server (VPS/Dedicated)

#### Using Gunicorn + Nginx

1. **Install Gunicorn**
```bash
pip install gunicorn
```

2. **Create Gunicorn systemd service**

File: `/etc/systemd/system/kortekstream.service`

```ini
[Unit]
Description=KortekStream Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/streaming-site
Environment="PATH=/path/to/streaming-site/venv/bin"
ExecStart=/path/to/streaming-site/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile /path/to/streaming-site/logs/gunicorn-access.log \
    --error-logfile /path/to/streaming-site/logs/gunicorn-error.log \
    mysite.wsgi:application

[Install]
WantedBy=multi-user.target
```

3. **Start Gunicorn service**
```bash
sudo systemctl start kortekstream
sudo systemctl enable kortekstream
sudo systemctl status kortekstream
```

4. **Configure Nginx**

File: `/etc/nginx/sites-available/kortekstream`

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /path/to/ssl/fullchain.pem;
    ssl_certificate_key /path/to/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Static files served by Nginx (WhiteNoise handles this, but can be optimized)
    location /static/ {
        alias /path/to/streaming-site/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }

    # Security headers
    add_header X-Frame-Options "DENY";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    # Logging
    access_log /var/log/nginx/kortekstream-access.log;
    error_log /var/log/nginx/kortekstream-error.log;
}
```

5. **Enable site and reload Nginx**
```bash
sudo ln -s /etc/nginx/sites-available/kortekstream /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Option 2: Docker Deployment

1. **Create Dockerfile**

```dockerfile
FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Install Node dependencies and build CSS
COPY package.json /app/
RUN npm install

# Copy project
COPY . /app/

# Build Tailwind CSS
RUN npm run build:css

# Collect static files
RUN python manage.py collectstatic --noinput

# Create logs directory
RUN mkdir -p /app/logs

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "mysite.wsgi:application"]
```

2. **Create docker-compose.yml**

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 --workers 3 mysite.wsgi:application
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=kortekstream
      - POSTGRES_USER=kortekstream
      - POSTGRES_PASSWORD=secure_password

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

### Option 3: Platform as a Service (Heroku, Railway, etc.)

#### Heroku Example

1. **Create Procfile**
```
web: gunicorn mysite.wsgi --log-file -
release: python manage.py migrate && python manage.py collectstatic --noinput
```

2. **Create runtime.txt**
```
python-3.14.0
```

3. **Deploy**
```bash
heroku create your-app-name
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
git push heroku master
```

## Post-Deployment Tasks

### 1. Verify Deployment

```bash
# Check Django
python manage.py check --deploy

# Test static files
curl https://yourdomain.com/static/css/output.css

# Check error pages
curl https://yourdomain.com/non-existent-page
```

### 2. Setup Monitoring

- Monitor application logs: `/path/to/logs/django.log`
- Monitor Gunicorn logs: `/path/to/logs/gunicorn-*.log`
- Monitor Nginx logs: `/var/log/nginx/kortekstream-*.log`
- Setup uptime monitoring (e.g., UptimeRobot, Pingdom)

### 3. Backup Strategy

```bash
# Backup database (if using SQLite)
cp db.sqlite3 backups/db.sqlite3.$(date +%Y%m%d_%H%M%S)

# Backup user uploads (if any)
tar -czf backups/media.tar.gz media/
```

### 4. SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Performance Optimization

### 1. Enable Compression in Nginx

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
```

### 2. Setup Redis for Caching (Optional)

```bash
pip install django-redis
```

Add to settings.py:
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

### 3. Database Connection Pooling (PostgreSQL)

```bash
pip install psycopg2-binary django-db-connection-pool
```

## Troubleshooting

### Static Files Not Loading

```bash
# Rebuild CSS
npm run build:css

# Recollect static files
python manage.py collectstatic --clear --noinput

# Check permissions
chmod -R 755 staticfiles/
```

### 500 Errors

```bash
# Check logs
tail -f logs/django.log
tail -f logs/gunicorn-error.log

# Verify settings
python manage.py check --deploy

# Test locally with DEBUG=False
DEBUG=False python manage.py runserver
```

### Database Issues

```bash
# Check migrations
python manage.py showmigrations

# Re-run migrations
python manage.py migrate --run-syncdb
```

## Rollback Procedure

```bash
# Rollback to previous commit
git log --oneline  # Find commit hash
git checkout <previous-commit-hash>

# Rebuild
npm run build:css
python manage.py collectstatic --noinput

# Restart service
sudo systemctl restart kortekstream
```

## Maintenance Mode

Create a simple maintenance page and configure Nginx:

```nginx
location / {
    if (-f $document_root/maintenance.html) {
        return 503;
    }
    # ... normal configuration
}

error_page 503 @maintenance;
location @maintenance {
    rewrite ^(.*)$ /maintenance.html break;
}
```

## Security Checklist

- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY set
- [ ] ALLOWED_HOSTS configured properly
- [ ] SSL/HTTPS enabled
- [ ] Security headers configured
- [ ] CSRF protection enabled
- [ ] SQL injection protection (using ORM)
- [ ] XSS protection enabled
- [ ] Regular security updates
- [ ] Firewall configured
- [ ] Database credentials secured
- [ ] Log file permissions set correctly

## Support

For deployment issues, check:
- Application logs: `logs/django.log`
- Error handling documentation: `ERROR_HANDLING_SUMMARY.md`
- Django deployment docs: https://docs.djangoproject.com/en/4.2/howto/deployment/
