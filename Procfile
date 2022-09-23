release: python manage.py migrate && sudo apt-get update && apt-get install libgl1 && sudo apt-get update && apt-get install -y python3-opencv && sudo apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
web: gunicorn test_monitor.wsgi --log-file -
celery: celery worker -A forum -l info