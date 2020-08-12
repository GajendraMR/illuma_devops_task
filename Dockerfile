FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk update && apk add build-base nodejs mariadb-dev tzdata git libxml2-dev libxslt-dev
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
