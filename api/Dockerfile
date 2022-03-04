FROM python:3.6-slim

RUN apt-get update && apt-get install -y git

WORKDIR /api

COPY requirements.txt /api/
RUN pip install -r /api/requirements.txt
