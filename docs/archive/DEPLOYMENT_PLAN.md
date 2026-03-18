# DEPLOYMENT SETUP PLAN

## Current Analysis

### Static Files Structure
```
static/
├── apple-touch-icon.png
├── favicon-16x16.png
├── favicon-32x32.png
├── favicon.ico
├── images/
│   └── og-image.jpg
├── js/
│   └── watchlist.js
└── og-image.jpg
```

### Tailwind CSS Status
- ❌ Currently using CDN: `https://cdn.tailwindcss.com`
- ❌ Not production-ready (CDN compiles on client-side)
- ✅ Custom config in base.html
- ⚠️ Need to setup build process for production

### Git Status
- ✅ Git repository already initialized
- ❌ No .gitignore file
- ✅ Working tree clean

### Requirements
- ✅ Django 6.0.3 installed
- ✅ python-decouple for env vars
- ❌ WhiteNoise not installed
- ❌ No production dependencies separated

## Implementation Plan

### Phase 1: WhiteNoise Setup
1. Install whitenoise package
2. Configure in Django settings
3. Add to middleware
4. Setup STATIC_ROOT for collectstatic
5. Test static file serving

### Phase 2: Tailwind Production Build
1. Install Node.js dependencies (tailwindcss, autoprefixer, postcss)
2. Create tailwind.config.js
3. Create input CSS file
4. Setup build script in package.json
5. Update base.html to use compiled CSS
6. Add build output to static files

### Phase 3: Git Configuration
1. Create comprehensive .gitignore
2. Exclude: venv, __pycache__, .env, db.sqlite3, logs, node_modules, static/css/output
3. Keep: static files (icons, js), templates, apps, requirements.txt
4. Document deployment process

### Phase 4: Production Settings
1. Separate dev/prod settings or use environment variables
2. Security settings (SECURE_HSTS, SSL_REDIRECT, etc)
3. Update .env.example with all required vars
4. Create deployment checklist

### Phase 5: Testing
1. Test collectstatic command
2. Test with DEBUG=False
3. Verify all static files served correctly
4. Test Tailwind compiled CSS
5. Verify no 404s on static files

## Files to Create/Modify

### Create:
- `.gitignore`
- `package.json` (for Tailwind)
- `tailwind.config.js`
- `static/css/input.css` (Tailwind source)
- `requirements-prod.txt` (production dependencies)
- `deploy.sh` (deployment script)
- `DEPLOYMENT_GUIDE.md`

### Modify:
- `requirements.txt` (add whitenoise)
- `mysite/settings.py` (whitenoise, static files config, security)
- `templates/base.html` (switch from CDN to compiled CSS)

## Success Criteria

✅ Static files served efficiently with WhiteNoise
✅ Tailwind CSS compiled for production (no CDN)
✅ Git properly configured with .gitignore
✅ All secrets in .env (not in repo)
✅ Works with DEBUG=False
✅ Production security settings configured
✅ Documentation complete
