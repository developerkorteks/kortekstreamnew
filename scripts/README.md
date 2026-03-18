# Scripts Directory

This directory contains utility scripts for deployment and maintenance.

## Available Scripts

### Deployment Scripts

#### `deploy.sh`
**Traditional deployment script**

Performs complete deployment:
- ✅ Checks virtual environment
- ✅ Validates .env file exists
- ✅ Warns if DEBUG=True
- ✅ Installs Python dependencies
- ✅ Installs Node.js dependencies
- ✅ Builds Tailwind CSS
- ✅ Runs Django checks
- ✅ Runs migrations
- ✅ Collects static files
- ✅ Creates logs directory

**Usage:**
```bash
./scripts/deploy.sh
```

---

#### `start_pm2.sh`
**Start application with PM2**

Production deployment with PM2 process manager:
- ✅ Validates environment
- ✅ Builds CSS
- ✅ Collects static files
- ✅ Runs migrations
- ✅ Starts Gunicorn with PM2 (port 63847)
- ✅ Auto-restart on crash
- ✅ Process monitoring

**Usage:**
```bash
# Direct
./scripts/start_pm2.sh

# Via npm (recommended)
npm run pm2:start
```

**Port**: 63847 (unique high port)

---

#### `stop_pm2.sh`
**Stop PM2 process**

Gracefully stops the application:
- Stops PM2 process
- Deletes from PM2 list
- Saves PM2 state

**Usage:**
```bash
# Direct
./scripts/stop_pm2.sh

# Via npm (recommended)
npm run pm2:stop
```

---

## PM2 Quick Commands

Using npm scripts (recommended):

```bash
npm run pm2:start      # Start application
npm run pm2:stop       # Stop application
npm run pm2:restart    # Restart application
npm run pm2:logs       # View logs (real-time)
npm run pm2:status     # Check status
npm run pm2:monit      # Interactive monitoring
```

---

## When to Use Each Script

### Development
```bash
# Watch CSS changes
npm run watch:css

# Run Django dev server (separate terminal)
python manage.py runserver
```

### Initial Deployment
```bash
# First time setup
./scripts/deploy.sh
```

### Production with PM2
```bash
# Start with process manager
npm run pm2:start

# Monitor
npm run pm2:monit

# View logs
npm run pm2:logs
```

### Updates
```bash
# Pull code
git pull

# Install deps
npm install
pip install -r requirements.txt

# Build & migrate
npm run build:css
python manage.py collectstatic --noinput
python manage.py migrate

# Restart (zero-downtime)
npm run pm2:restart
```

---

## Logs

All scripts create logs in `logs/` directory:

- `django.log` - Django application logs
- `gunicorn-access.log` - HTTP access logs
- `gunicorn-error.log` - Gunicorn errors
- `pm2-out.log` - PM2 stdout
- `pm2-error.log` - PM2 stderr
- `pm2-combined.log` - Combined PM2 logs

View logs:
```bash
# Real-time Django logs
tail -f logs/django.log

# Real-time all errors
tail -f logs/*error.log

# PM2 logs
npm run pm2:logs
```

---

## Prerequisites

### For deploy.sh
- Virtual environment activated
- `.env` file exists
- Node.js and npm installed

### For PM2 scripts
- PM2 installed: `npm install`
- Gunicorn in venv: `pip install gunicorn`
- Port 63847 available

---

## Troubleshooting

### Script won't execute
```bash
# Make executable
chmod +x scripts/*.sh
```

### PM2 command not found
```bash
# Install PM2
npm install

# Use full path
./node_modules/.bin/pm2 status
```

### Port already in use
```bash
# Find process
lsof -i :63847

# Kill if needed
kill -9 <PID>

# Or use different port in ecosystem.config.js
```

### Permission denied
```bash
# Fix permissions
chmod +x scripts/*.sh
```

---

## Documentation

- **Deployment Guide**: `../DEPLOYMENT_GUIDE.md`
- **PM2 Deployment**: `../docs/PM2_DEPLOYMENT.md`
- **Error Handling**: `../ERROR_HANDLING_SUMMARY.md`

---

## Adding New Scripts

When adding new scripts to this directory:
1. Make them executable: `chmod +x scripts/your_script.sh`
2. Add documentation here
3. Follow naming convention: `lowercase_with_underscores.sh`
4. Add error handling and logging
5. Test thoroughly before committing
