#!/bin/sh

# Wait for a moment to ensure everything is ready
sleep 2

# Create database directory if it doesn't exist
mkdir -p /app/db

# Run migrations
python manage.py migrate

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 LockLink.wsgi:application 