#!/bin/bash
# Deployment script for KortekStream

set -e  # Exit on error

echo "======================================"
echo "KortekStream Deployment Script"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${RED}Error: Virtual environment is not activated${NC}"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create .env file from .env.example"
    exit 1
fi

# Check DEBUG setting
DEBUG=$(python -c "from decouple import config; print(config('DEBUG', default='True'))")
if [ "$DEBUG" == "True" ]; then
    echo -e "${YELLOW}Warning: DEBUG is set to True${NC}"
    read -p "Are you sure you want to deploy with DEBUG=True? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled"
        exit 1
    fi
fi

echo "Step 1: Installing/Updating Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 2: Installing/Updating Node.js dependencies..."
npm install

echo ""
echo "Step 3: Building Tailwind CSS for production..."
npm run build:css

echo ""
echo "Step 4: Running Django checks..."
python manage.py check --deploy

echo ""
echo "Step 5: Running migrations..."
python manage.py migrate --noinput

echo ""
echo "Step 6: Collecting static files..."
python manage.py collectstatic --noinput --clear

echo ""
echo "Step 7: Creating logs directory..."
mkdir -p logs

echo ""
echo -e "${GREEN}======================================"
echo "Deployment completed successfully!"
echo "======================================${NC}"
echo ""
echo "Next steps:"
echo "1. Restart your application server (Gunicorn/uWSGI)"
echo "2. Reload your web server (Nginx/Apache)"
echo "3. Check logs for any errors"
echo ""
echo "Example commands:"
echo "  sudo systemctl restart kortekstream"
echo "  sudo systemctl reload nginx"
echo ""
