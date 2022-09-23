release: python manage.py migrate && sudo apt-get update && apt-get install -y python3-opencv && pip install opencv-python 
web: gunicorn test_monitor.wsgi --log-file -
celery: celery worker -A forum -l info