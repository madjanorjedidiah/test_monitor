release: python manage.py migrate && sudo apt-get install redis-server
redis: redis-server
web: gunicorn test_monitor.wsgi --log-file -
celery: celery worker -A forum -l info