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

RUN pip install -r /home/appuser/test_monitor/requirements.txt

COPY .  /home/appuser/test_monitor

