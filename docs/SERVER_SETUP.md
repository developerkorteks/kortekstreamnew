# Server Setup Guide - Production Server

Configuration for production server: r-server68714-vv3

## Server Information

**Hostname**: r-server68714-vv3
**User**: root
**Project Path**: /root/kortekstreamnew
**Python**: /root/kortekstreamnew/venv/bin/python
**Domain**: kortekstream.online

## Initial Server Setup

### 1. System Requirements

```bash
# Update system
apt-get update
apt-get upgrade -y

# Install required packages
apt-get install -y python3 python3-pip python3-venv nodejs npm nginx git curl

# Install PM2 globally (optional, or use local)
npm install -g pm2
```

### 2. Project Setup

```bash
# Navigate to project
cd /root/kortekstreamnew

# Verify files
ls -la
# Should see: ads, db.sqlite3, docs, ecosystem.config.js, logs, manage.py, etc.

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify Python path
which python
# Should be: /root/kortekstreamnew/venv/bin/python

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install

# Build Tailwind CSS
npm run build:css

# Create logs directory
mkdir -p logs
```

### 3. Environment Configuration

```bash
# Create .env file
cp .env.example .env

# Edit .env
nano .env
```

Set the following in `.env`:

```env
DEBUG=False
SECRET_KEY=your-secure-random-key-here

# Domain
ALLOWED_HOSTS=kortekstream.online,www.kortekstream.online

# CSRF
CSRF_TRUSTED_ORIGINS=https://kortekstream.online,https://www.kortekstream.online

# API
STREAMEX_API_BASE_URL=http://localhost:5000/api
API_TIMEOUT=30
```

### 4. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## PM2 Configuration

### Current Configuration

**File**: `ecosystem.config.js`

```javascript
{
  name: 'kortekstream',
  script: './venv/bin/gunicorn',
  args: 'mysite.wsgi:application --bind 0.0.0.0:63847 --workers 3',
  cwd: '/root/kortekstreamnew',
  env: {
    PATH: '/root/kortekstreamnew/venv/bin:' + process.env.PATH,
  }
}
```

### Start Application

```bash
# Using npm script
npm run pm2:start

# Or using PM2 directly
pm2 start ecosystem.config.js

# Check status
pm2 status

# View logs
pm2 logs kortekstream

# Monitor
pm2 monit
```

### PM2 Startup (Auto-start on reboot)

```bash
# Generate startup script
pm2 startup

# It will show a command like:
# sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u root --hp /root

# Run that command, then save PM2 process list
pm2 save
```

### PM2 Commands

```bash
# Start
pm2 start kortekstream

# Stop
pm2 stop kortekstream

# Restart
pm2 restart kortekstream

# Delete
pm2 delete kortekstream

# Logs
pm2 logs kortekstream

# Logs (last 100 lines)
pm2 logs kortekstream --lines 100

# Clear logs
pm2 flush

# Monitor
pm2 monit

# List all processes
pm2 list
```

## Nginx Configuration

### Install Nginx

```bash
apt-get install -y nginx
```

### Configure Site

Create `/etc/nginx/sites-available/kortekstream`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name kortekstream.online www.kortekstream.online;

    # Let's Encrypt ACME challenge
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Redirect to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name kortekstream.online www.kortekstream.online;

    # SSL Configuration (will be managed by Certbot)
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

    # Static Files
    location /static/ {
        alias /root/kortekstreamnew/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Proxy to Gunicorn (port 63847)
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
    }

    # Logging
    access_log /var/log/nginx/kortekstream-access.log;
    error_log /var/log/nginx/kortekstream-error.log;
}
```

### Enable Site

```bash
# Create symlink
ln -s /etc/nginx/sites-available/kortekstream /etc/nginx/sites-enabled/

# Test configuration
nginx -t

# Reload Nginx
systemctl reload nginx
```

## SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
apt-get install -y certbot python3-certbot-nginx

# Get certificate
certbot --nginx -d kortekstream.online -d www.kortekstream.online

# Follow prompts, select:
# - Redirect HTTP to HTTPS: Yes

# Test auto-renewal
certbot renew --dry-run

# Certificate will auto-renew every 90 days
```

## Firewall Configuration

```bash
# Install UFW
apt-get install -y ufw

# Allow SSH (important!)
ufw allow 22

# Allow HTTP and HTTPS
ufw allow 80
ufw allow 443

# Enable firewall
ufw enable

# Check status
ufw status
```

## Verification

### 1. Check Python Environment

```bash
source venv/bin/activate
which python
# Should be: /root/kortekstreamnew/venv/bin/python

python --version
# Should be: Python 3.x
```

### 2. Check Gunicorn

```bash
source venv/bin/activate
which gunicorn
# Should be: /root/kortekstreamnew/venv/bin/gunicorn

# Test Gunicorn manually
gunicorn mysite.wsgi:application --bind 0.0.0.0:63847
# Press Ctrl+C to stop
```

### 3. Check PM2

```bash
pm2 status
# Should show: kortekstream | online

pm2 logs kortekstream --lines 50
# Check for errors
```

### 4. Check Application

```bash
# Local test
curl http://localhost:63847
# Should return HTML

# Domain test (after SSL setup)
curl https://kortekstream.online
# Should return HTML
```

## Troubleshooting

### PM2 Won't Start

```bash
# Check logs
pm2 logs kortekstream --err

# Delete and restart
pm2 delete kortekstream
pm2 start ecosystem.config.js

# Check Gunicorn manually
source venv/bin/activate
gunicorn mysite.wsgi:application --bind 0.0.0.0:63847
```

### Permission Issues

```bash
# Fix ownership
chown -R root:root /root/kortekstreamnew

# Fix logs directory
chmod 755 logs
```

### Port Already in Use

```bash
# Check what's using port 63847
lsof -i :63847

# Kill process if needed
kill -9 <PID>
```

### Nginx Errors

```bash
# Test config
nginx -t

# Check error log
tail -f /var/log/nginx/error.log

# Restart Nginx
systemctl restart nginx
```

## Maintenance

### Update Application

```bash
cd /root/kortekstreamnew
git pull
source venv/bin/activate
pip install -r requirements.txt
npm install
npm run build:css
python manage.py migrate
python manage.py collectstatic --noinput
pm2 restart kortekstream
```

### View Logs

```bash
# PM2 logs
pm2 logs kortekstream

# Django logs
tail -f /root/kortekstreamnew/logs/django.log

# Gunicorn logs
tail -f /root/kortekstreamnew/logs/gunicorn-error.log

# Nginx logs
tail -f /var/log/nginx/kortekstream-error.log
```

### Backup

```bash
# Database
cp /root/kortekstreamnew/db.sqlite3 /root/backups/db-$(date +%Y%m%d).sqlite3

# .env file
cp /root/kortekstreamnew/.env /root/backups/.env-$(date +%Y%m%d)
```

## Quick Reference

**Project Path**: `/root/kortekstreamnew`
**Activate venv**: `source venv/bin/activate`
**Start PM2**: `npm run pm2:start`
**View logs**: `pm2 logs kortekstream`
**Restart**: `pm2 restart kortekstream`
**Nginx reload**: `systemctl reload nginx`

Your server is configured and ready! 🚀
