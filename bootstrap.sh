#!/bin/sh

# Start up nginx, which will fork into the background
nginx -p /app/exposure-front -c nginx.conf

# Then, start up gunicorn which will remain in the foreground
cd /app/exposure-back || (echo "Failed to change into /app/exposure-back directory"; exit 1)
gunicorn -b '127.0.0.1:8001' -w 4 'exposure:app'
