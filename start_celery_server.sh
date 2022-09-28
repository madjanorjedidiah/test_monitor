#!/usr/bin/env bash

celery -A test_monitor worker -l info

# echo "Running migrations.."
# python manage.py migrate
# echo "Starting server.."
# python manage.py runserver 0.0.0.0:8000