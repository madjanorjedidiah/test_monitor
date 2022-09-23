release: python manage.py migrate && pip3 install pyautogui && sudo -H pip3 install pyautogui && sudo apt-get install xauth
web: gunicorn test_monitor.wsgi --log-file -
celery: celery worker -A forum -l info