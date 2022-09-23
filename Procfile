release: python manage.py migrate &&  echo "DISPLAY=:0" >> ~/.bashrc && source ~/.bashrc && export DISPLAY=:0
web: gunicorn test_monitor.wsgi --log-file -
celery: celery worker -A forum -l info