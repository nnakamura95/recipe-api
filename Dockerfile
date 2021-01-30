FROM python:3.9.1-alpine
MAINTAINER NLN DEV

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D nakamura
USER nakamura
