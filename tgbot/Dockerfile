FROM python:3.11
WORKDIR /tgbot

COPY ./tgbot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./tgbot ./tgbot
COPY .env .