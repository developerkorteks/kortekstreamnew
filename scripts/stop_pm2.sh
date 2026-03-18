#!/bin/bash
# Stop KortekStream PM2 process

echo "🛑 Stopping KortekStream..."
./node_modules/.bin/pm2 stop kortekstream
./node_modules/.bin/pm2 delete kortekstream
./node_modules/.bin/pm2 save
echo "✓ KortekStream stopped successfully!"
