FROM python:3.8-slim-buster

WORKDIR /app

COPY app/ .
COPY .env .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["./main.py"]

