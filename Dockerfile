# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN apt-get update && apt-get install
RUN apt-get install -y libpq-dev

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install psycopg2-binary
RUN pip3 install -r requirements.txt
RUN pip3 install pytest
COPY start.sh /usr/bin/start.sh
RUN chmod +x /usr/bin/start.sh
CMD [ "sh", "/usr/bin/start.sh"]