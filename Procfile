release: python manage.py migrate && pip3 install pyautogui
web: gunicorn test_monitor.wsgi --log-file -
celery: celery worker -A forum -l info