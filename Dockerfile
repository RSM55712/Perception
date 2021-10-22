FROM tiangolo/uwsgi-nginx-flask:python3.7

LABEL maintainer "Rohit Mukund>"

RUN apt-get update && apt-get install -y \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.txt /
RUN pip install --requirement /requirements.txt

RUN python -m nltk.downloader punkt

COPY ./app /app

ENV LISTEN_PORT=8000
EXPOSE 8000
