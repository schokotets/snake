FROM python:3.8-slim-buster

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

EXPOSE 8080 8090

COPY ./server .

CMD ["python3", "server.py"]