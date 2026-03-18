# KortekStream - Premium Streaming Platform

A modern Django-based streaming platform that aggregates content from multiple sources with a beautiful, responsive UI.

## Features

✅ **Multi-Source Content Aggregation**
- Movies, TV Shows, and Anime
- Real-time streaming from multiple providers
- Advanced search functionality

✅ **Modern UI/UX**
- Built with Tailwind CSS
- Responsive design
- Smooth animations and transitions
- Dark theme optimized

✅ **Production Ready**
- WhiteNoise for efficient static file serving
- Comprehensive error handling
- Security best practices
- Environment-based configuration

✅ **SEO Optimized**
- Meta tags and Open Graph support
- Sitemap generation
- Robots.txt configuration

## Technology Stack

- **Backend**: Django 6.0.3
- **Frontend**: Tailwind CSS 3.4
- **Static Files**: WhiteNoise 6.12
- **API Client**: Requests
- **Config**: python-decouple

## Quick Start

### Prerequisites
- Python 3.14+
- Node.js 11+ and npm
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd streaming-site
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Node.js dependencies**
```bash
npm install
```

5. **Build Tailwind CSS**
```bash
npm run build:css
```

6. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

7. **Run migrations**
```bash
python manage.py migrate
```

8. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

9. **Run development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Development

### Watch Tailwind CSS changes
```bash
npm run watch:css
```

### Run with auto-reload
```bash
python manage.py runserver
```

## Production Deployment

### Environment Configuration

Set these in your `.env` file:

```env
DEBUG=False
SECRET_KEY=your-secure-random-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# API Configuration
STREAMEX_API_BASE_URL=http://your-api-url/api
API_TIMEOUT=30
```

### Build Steps

1. **Build Tailwind CSS for production**
```bash
npm run build:css
```

2. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

3. **Check deployment readiness**
```bash
python manage.py check --deploy
```

### Static Files

Static files are served using WhiteNoise with compression and caching:
- All static files are automatically compressed (gzip/brotli)
- Far-future cache headers for immutable files
- Manifest-based cache busting

## Project Structure

```
streaming-site/
├── mysite/              # Django project settings
│   ├── settings.py      # Main settings
│   ├── urls.py          # URL configuration
│   └── middleware.py    # Custom middleware
├── streaming/           # Main app
│   ├── views.py         # View logic
│   ├── services.py      # API client
│   └── templatetags/    # Template tags
├── ads/                 # Ad integration app
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── 404.html         # Error pages
│   ├── 500.html
│   └── streaming/       # App templates
├── static/              # Static source files
│   ├── css/
│   │   ├── input.css    # Tailwind input
│   │   └── output.css   # Compiled CSS (generated)
│   ├── js/
│   └── images/
├── staticfiles/         # Collected static files (generated)
├── logs/                # Application logs
├── package.json         # Node.js dependencies
├── tailwind.config.js   # Tailwind configuration
└── requirements.txt     # Python dependencies
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode (False in production) | `True` |
| `SECRET_KEY` | Django secret key | Required |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `*` |
| `STREAMEX_API_BASE_URL` | Backend API URL | `http://localhost:5000/api` |
| `API_TIMEOUT` | API request timeout (seconds) | `30` |

## Error Handling

The application includes comprehensive error handling:
- Custom 404, 500, 403, 400 error pages
- All errors logged server-side
- User-friendly error messages (no technical details exposed)
- Automatic error reporting via middleware

See `ERROR_HANDLING_SUMMARY.md` for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue in the repository.
