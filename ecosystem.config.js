/**
 * PM2 Ecosystem Configuration for KortekStream
 * Deploy Django application with Gunicorn
 */

module.exports = {
  apps: [
    {
      name: 'kortekstream',
      script: 'venv/bin/gunicorn',
      args: 'mysite.wsgi:application --bind 0.0.0.0:63847 --workers 3 --timeout 120 --access-logfile logs/gunicorn-access.log --error-logfile logs/gunicorn-error.log',
      cwd: '/home/korteks/Data/project/frontend/frontend',
      interpreter: 'none', // Use the script directly (gunicorn from venv)
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production',
        PORT: 63847,
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 63847,
      },
      error_file: 'logs/pm2-error.log',
      out_file: 'logs/pm2-out.log',
      log_file: 'logs/pm2-combined.log',
      time: true,
      merge_logs: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    },
  ],

  deploy: {
    production: {
      user: 'korteks',
      host: 'localhost',
      ref: 'origin/master',
      repo: 'git@github.com:yourusername/kortekstream.git',
      path: '/home/korteks/Data/project/frontend/frontend',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && npm run build:css && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && pm2 reload ecosystem.config.js --env production',
      'pre-setup': '',
    },
  },
};
