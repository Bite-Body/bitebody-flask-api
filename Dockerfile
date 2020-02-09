FROM python:3.8-slim

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD python ./manage.py