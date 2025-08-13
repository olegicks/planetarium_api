FROM python:3.11.6-alpine3.18
LABEL maintainer="sholeg2005@gmail.com"

WORKDIR / planetarium

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /files/media


RUN adduser \
    --disabled-password \
    --no-create-home \
    user

RUN chown -R user /files/media
RUN chmod -R 755 /files/media

USER user