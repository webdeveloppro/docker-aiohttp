FROM python:3.6.2

RUN mkdir -p /opt/app
COPY . /opt/app

WORKDIR /opt/app

RUN pip install --no-cache-dir -r requirements.txt
