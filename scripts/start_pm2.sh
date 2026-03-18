#!/bin/bash
# Start KortekStream with PM2
# Port: 63847 (unique high port)

set -e

echo "═══════════════════════════════════════════════════════════"
echo "🚀 Starting KortekStream with PM2"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found${NC}"
    echo "Please create it first: python -m venv venv"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create it from .env.example"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}✓${NC} Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies if needed
echo -e "${GREEN}✓${NC} Checking dependencies..."
pip install -q gunicorn 2>/dev/null || echo "Gunicorn already installed"

# Build Tailwind CSS
echo -e "${GREEN}✓${NC} Building Tailwind CSS..."
npm run build:css > /dev/null 2>&1

# Collect static files
echo -e "${GREEN}✓${NC} Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1

# Run migrations
echo -e "${GREEN}✓${NC} Running migrations..."
python manage.py migrate --noinput > /dev/null 2>&1

# Create logs directory if not exists
mkdir -p logs

# Stop existing PM2 process if running
echo -e "${GREEN}✓${NC} Checking for existing PM2 process..."
./node_modules/.bin/pm2 stop kortekstream 2>/dev/null || echo "No existing process to stop"
./node_modules/.bin/pm2 delete kortekstream 2>/dev/null || echo "No existing process to delete"

# Start with PM2
echo -e "${GREEN}✓${NC} Starting application with PM2..."
./node_modules/.bin/pm2 start ecosystem.config.js

# Save PM2 process list
./node_modules/.bin/pm2 save

# Display status
echo ""
echo "═══════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ KortekStream started successfully!${NC}"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📊 Application Info:"
echo "   Name:  kortekstream"
echo "   Port:  63847"
echo "   URL:   http://localhost:63847"
echo ""
echo "📝 Useful PM2 Commands:"
echo "   pm2 status                  # Check status"
echo "   pm2 logs kortekstream       # View logs"
echo "   pm2 restart kortekstream    # Restart app"
echo "   pm2 stop kortekstream       # Stop app"
echo "   pm2 delete kortekstream     # Delete app"
echo "   pm2 monit                   # Monitor app"
echo ""
echo "🌐 Access your app at: http://localhost:63847"
echo ""
