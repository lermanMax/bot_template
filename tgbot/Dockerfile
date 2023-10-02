FROM python:3
WORKDIR /tgbot

COPY ./tgbot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./tgbot ./tgbot
COPY .env .