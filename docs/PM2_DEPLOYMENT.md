# PM2 Deployment Guide - KortekStream

Complete guide for deploying KortekStream using PM2 process manager.

## Overview

**Application**: KortekStream
**Port**: 63847 (unique high port, rarely used)
**Process Manager**: PM2
**Web Server**: Gunicorn
**Workers**: 3

## Quick Start

### 1. Install Dependencies

```bash
# Install PM2 (already in package.json)
npm install

# Verify PM2 installation
./node_modules/.bin/pm2 --version
```

### 2. Start Application

```bash
# Using npm script (recommended)
npm run pm2:start

# Or directly
./scripts/start_pm2.sh
```

### 3. Check Status

```bash
npm run pm2:status
# Or: ./node_modules/.bin/pm2 status
```

## Configuration

### Port Configuration

**Port**: 63847
- High port number (60000+)
- Rarely used
- No conflicts with common services

To change port, edit:
1. `ecosystem.config.js` - Update `args` and `env.PORT`
2. `.env` - Add `PORT=63847` if needed

### PM2 Ecosystem Config

File: `ecosystem.config.js`

```javascript
{
  name: 'kortekstream',
  script: 'venv/bin/gunicorn',
  args: 'mysite.wsgi:application --bind 0.0.0.0:63847 --workers 3',
  instances: 1,
  autorestart: true,
  max_memory_restart: '500M',
}
```

**Key settings:**
- **name**: Process name (kortekstream)
- **workers**: 3 (adjust based on CPU cores)
- **timeout**: 120s (for long requests)
- **autorestart**: true (auto-restart on crash)
- **max_memory_restart**: 500MB (restart if exceeds)

### Gunicorn Configuration

**Workers**: 3
**Timeout**: 120 seconds
**Bind**: 0.0.0.0:63847

Log files:
- Access: `logs/gunicorn-access.log`
- Error: `logs/gunicorn-error.log`

## PM2 Commands

### Using NPM Scripts (Recommended)

```bash
# Start application
npm run pm2:start

# Stop application
npm run pm2:stop

# Restart application
npm run pm2:restart

# View logs
npm run pm2:logs

# Check status
npm run pm2:status

# Monitor (interactive)
npm run pm2:monit
```

### Using PM2 Directly

```bash
# Start
./node_modules/.bin/pm2 start ecosystem.config.js

# Stop
./node_modules/.bin/pm2 stop kortekstream

# Restart
./node_modules/.bin/pm2 restart kortekstream

# Delete (stop and remove)
./node_modules/.bin/pm2 delete kortekstream

# Logs
./node_modules/.bin/pm2 logs kortekstream

# Monitor
./node_modules/.bin/pm2 monit

# List all processes
./node_modules/.bin/pm2 list

# Show process details
./node_modules/.bin/pm2 show kortekstream

# Save process list (persist across reboots)
./node_modules/.bin/pm2 save

# Resurrect saved processes
./node_modules/.bin/pm2 resurrect
```

## Accessing the Application

Once started, access at:
- **Local**: http://localhost:63847
- **Network**: http://YOUR_IP:63847

Make sure port 63847 is open in firewall if accessing from network.

## Logs

### PM2 Logs
```bash
# Real-time logs
npm run pm2:logs

# Or specify lines
./node_modules/.bin/pm2 logs kortekstream --lines 100
```

### Application Logs

Locations:
- **Django**: `logs/django.log`
- **Gunicorn Access**: `logs/gunicorn-access.log`
- **Gunicorn Error**: `logs/gunicorn-error.log`
- **PM2 Output**: `logs/pm2-out.log`
- **PM2 Error**: `logs/pm2-error.log`

View logs:
```bash
# Django logs
tail -f logs/django.log

# Gunicorn access
tail -f logs/gunicorn-access.log

# Gunicorn errors
tail -f logs/gunicorn-error.log

# All errors
tail -f logs/*error.log
```

## Auto-Startup (Optional)

To make PM2 start on system boot:

```bash
# Generate startup script
./node_modules/.bin/pm2 startup

# Follow the instructions printed
# Usually something like:
sudo env PATH=$PATH:/usr/bin /path/to/pm2 startup systemd -u USERNAME --hp /home/USERNAME

# Save current process list
./node_modules/.bin/pm2 save
```

## Nginx Reverse Proxy (Recommended for Production)

For production, put Nginx in front:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:63847;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Monitoring

### PM2 Monitor

```bash
# Interactive monitoring
npm run pm2:monit

# Or
./node_modules/.bin/pm2 monit
```

Shows:
- CPU usage
- Memory usage
- Process status
- Logs in real-time

### PM2 Web Interface (Optional)

```bash
./node_modules/.bin/pm2 web

# Access at: http://localhost:9615
```

## Troubleshooting

### Application Won't Start

```bash
# Check logs
npm run pm2:logs

# Check status
npm run pm2:status

# Check if port is already in use
lsof -i :63847
# Or: netstat -tulpn | grep 63847

# Restart PM2 daemon
./node_modules/.bin/pm2 kill
./node_modules/.bin/pm2 resurrect
```

### High Memory Usage

If memory usage is high:

1. Check `ecosystem.config.js` - lower `max_memory_restart`
2. Reduce Gunicorn workers (edit `ecosystem.config.js` args)
3. Monitor with: `npm run pm2:monit`

### Port Already in Use

```bash
# Find process using port
lsof -i :63847

# Kill process
kill -9 <PID>

# Or choose different port in ecosystem.config.js
```

### Logs Growing Too Large

```bash
# Install PM2 log rotation
npm install pm2-logrotate

# Configure
./node_modules/.bin/pm2 install pm2-logrotate
./node_modules/.bin/pm2 set pm2-logrotate:max_size 10M
./node_modules/.bin/pm2 set pm2-logrotate:retain 7
```

## Performance Tuning

### Workers

Recommended: `(CPU cores * 2) + 1`

Example:
- 2 cores → 5 workers
- 4 cores → 9 workers

Edit in `ecosystem.config.js`:
```javascript
args: '... --workers 5 ...'
```

### Memory

If you have limited RAM, reduce workers:
```javascript
args: '... --workers 2 ...'
max_memory_restart: '300M'
```

## Deployment Workflow

### Development

```bash
# Watch CSS changes
npm run watch:css

# Run Django dev server (separate terminal)
python manage.py runserver
```

### Staging/Production

```bash
# Build CSS
npm run build:css

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start with PM2
npm run pm2:start

# Monitor
npm run pm2:logs
```

### Updates

```bash
# Pull latest code
git pull

# Install dependencies
npm install
pip install -r requirements.txt

# Build & collect
npm run build:css
python manage.py collectstatic --noinput

# Migrate
python manage.py migrate

# Reload (zero-downtime)
npm run pm2:restart
```

## Security Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use strong `SECRET_KEY`
- [ ] Setup firewall (only allow port 63847 from trusted IPs)
- [ ] Use Nginx reverse proxy with SSL
- [ ] Keep PM2 and dependencies updated
- [ ] Monitor logs regularly
- [ ] Setup log rotation
- [ ] Backup database regularly

## Support

For issues:
- Check logs: `npm run pm2:logs`
- PM2 docs: https://pm2.keymetrics.io/
- Django docs: https://docs.djangoproject.com/
- Gunicorn docs: https://docs.gunicorn.org/

## Summary

**Port**: 63847
**Start**: `npm run pm2:start`
**Stop**: `npm run pm2:stop`
**Logs**: `npm run pm2:logs`
**URL**: http://localhost:63847

Your application is now running with PM2! 🚀
