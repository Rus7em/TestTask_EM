FROM python:3.12.4-slim

ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_NAME
ARG DB_HOST

ENV DB_USERNAME=${DB_USERNAME}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_NAME=${DB_NAME}
ENV DB_HOST=${DB_HOST}

WORKDIR /code

copy ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

copy ./src /code/src


