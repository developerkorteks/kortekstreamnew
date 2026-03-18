# KortekStream - Premium Streaming Platform

A modern Django-based streaming platform that aggregates content from multiple sources with a beautiful, responsive UI.

**Live Domain**: [kortekstream.online](https://kortekstream.online)

## 🚀 Quick Start

### Development

```bash
# Clone repository
git clone <repository-url>
cd kortekstream

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
npm install

# Build CSS
npm run build:css

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver
```

### Production with PM2

```bash
# Start application
npm run pm2:start

# Access at http://localhost:63847
# Or https://kortekstream.online (if deployed)
```

## 📊 Features

- ✅ **Multi-Source Content**: Movies, TV Shows, and Anime
- ✅ **Modern UI**: Built with Tailwind CSS
- ✅ **Responsive Design**: Mobile-first approach
- ✅ **SEO Optimized**: Meta tags, sitemap, robots.txt
- ✅ **Production Ready**: WhiteNoise, PM2, comprehensive error handling
- ✅ **Security**: CSRF protection, HTTPS, HSTS, security headers

## 🛠️ Technology Stack

- **Backend**: Django 6.0.3
- **Frontend**: Tailwind CSS 3.4
- **Static Files**: WhiteNoise 6.12
- **Process Manager**: PM2 6.0.14
- **Web Server**: Gunicorn 25.1.0
- **API Client**: Requests

## 📚 Documentation

- **[Domain Setup](docs/DOMAIN_SETUP.md)** - kortekstream.online configuration
- **[PM2 Deployment](docs/PM2_DEPLOYMENT.md)** - Production deployment with PM2
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - General deployment instructions
- **[Error Handling](docs/ERROR_HANDLING_SUMMARY.md)** - Error handling implementation

## 🎯 Project Structure

```
kortekstream/
├── docs/                   # Documentation
├── mysite/                 # Django project
├── streaming/              # Main app
├── ads/                    # Ads integration
├── templates/              # HTML templates
├── static/                 # Static source files
├── scripts/                # Deployment scripts
├── .env                    # Environment config
├── ecosystem.config.js     # PM2 configuration
└── package.json            # Node dependencies
```

## 🔧 Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```env
DEBUG=False
SECRET_KEY=your-secure-random-key
ALLOWED_HOSTS=kortekstream.online,www.kortekstream.online
CSRF_TRUSTED_ORIGINS=https://kortekstream.online,https://www.kortekstream.online
STREAMEX_API_BASE_URL=http://localhost:5000/api
```

### Domain Configuration

**Domain**: kortekstream.online
**Port**: 63847 (internal, proxied by Nginx)

See [docs/DOMAIN_SETUP.md](docs/DOMAIN_SETUP.md) for complete setup.

## 🚀 Deployment

### PM2 (Production)

```bash
# Start
npm run pm2:start

# Stop
npm run pm2:stop

# Restart
npm run pm2:restart

# Logs
npm run pm2:logs

# Monitor
npm run pm2:monit
```

See [docs/PM2_DEPLOYMENT.md](docs/PM2_DEPLOYMENT.md) for details.

## 📝 Development Commands

```bash
# Watch CSS changes
npm run watch:css

# Build production CSS
npm run build:css

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Run migrations
python manage.py migrate
```

## 🔒 Security

- ✅ CSRF protection configured
- ✅ HTTPS enforced (production)
- ✅ HSTS enabled (1 year)
- ✅ Secure cookies
- ✅ XSS protection
- ✅ Content type sniffing protection
- ✅ Clickjacking protection

## 📊 Performance

- ✅ WhiteNoise for static files (compression + caching)
- ✅ Tailwind CSS compiled (31KB minified)
- ✅ CDN-free (no external dependencies)
- ✅ PM2 process management
- ✅ Gunicorn with 3 workers

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License

## 🙏 Support

For issues and questions, see documentation in `docs/` directory or open an issue.

---

**Live at**: [https://kortekstream.online](https://kortekstream.online)
