FROM python:3.6-slim

RUN apt-get update && apt-get install -y git gcc libpcre3-dev

WORKDIR /api

COPY requirements.txt /api/
RUN pip install -r /api/requirements.txt
