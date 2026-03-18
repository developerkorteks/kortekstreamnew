# Scripts Directory

This directory contains utility scripts for deployment and maintenance.

## Available Scripts

### `deploy.sh`
**Automated deployment script for production**

Performs complete deployment in one command:
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
# Make executable (first time only)
chmod +x scripts/deploy.sh

# Run deployment
./scripts/deploy.sh
```

**Prerequisites:**
- Virtual environment must be activated
- `.env` file must exist
- Node.js and npm installed

**Post-deployment:**
After running the script, you need to:
1. Restart your application server (Gunicorn/uWSGI)
2. Reload your web server (Nginx/Apache)

Example:
```bash
sudo systemctl restart kortekstream
sudo systemctl reload nginx
```

## Adding New Scripts

When adding new scripts to this directory:
1. Make them executable: `chmod +x scripts/your_script.sh`
2. Add documentation here
3. Follow naming convention: `lowercase_with_underscores.sh`
