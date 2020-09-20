FROM python:3.7.9-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y ffmpeg  # TAKES 450 MB!!!

COPY . .

RUN pip install -r requirements.txt

CMD python ./bot.py
