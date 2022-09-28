From python:3.8-slim as py_base


# set up env variables
ENV PYTHOONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN addgroup --system appuser \
    && adduser --system --ingroup appuser appuser

USER appuser

RUN mkdir /home/appuser/test_monitor
WORKDIR  /home/appuser/test_monitor

COPY requirements.txt /home/appuser/test_monitor

USER root
RUN pip install -r /home/appuser/test_monitor/requirements.txt

COPY --chown=appuser:appuser start_celery_server.sh /usr/local/bin

RUN chmod +x /usr/local/bin/start_celery_server.sh

USER appuser
COPY --chown=appuser:appuser . /home/appuser/test_monitor
RUN chmod -R 777 /home/appuser/test_monitor/start_celery_server.sh


