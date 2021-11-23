FROM python:3.9

WORKDIR /app

RUN apt-get update -u && apt-get install -y \
        supervisor \
        netcat

RUN supervisord

COPY requirements.txt .

RUN pip install -r requirements.txt
