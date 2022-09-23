release: python manage.py migrate
web: gunicorn test_monitor.wsgi --log-file -
celery: celery worker -A forum -l info