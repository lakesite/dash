FROM tiangolo/meinheld-gunicorn:python3.7-alpine3.8

LABEL maintainer="andy@lakesite.net"

RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc libc-dev

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
