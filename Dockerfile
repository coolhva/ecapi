FROM python:3.6-alpine

RUN adduser -D ecapi
WORKDIR /home/ecapi

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY ecapi.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV LOG_TO_STDOUT True
ENV FLASK_APP ecapi.py

RUN chown -R ecapi:ecapi ./
USER ecapi

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]