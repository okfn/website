FROM node:7.7-alpine

MAINTAINER Damjan Velickovski <damjan.velickovski@keitaro.com>

ENV LANG=en_US.UTF-8 \
    APP_DIR=/srv/app

COPY . ${APP_DIR}

WORKDIR ${APP_DIR}

RUN apk add --no-cache \
    bash \
	python \
	py-pip \
	git

RUN apk add --no-cache \
	build-base \
	gcc \
	g++ \
	python-dev \
	musl-dev \
	libjpeg-turbo-dev \
	libpng \
	freetype-dev \
	zlib-dev \
	postgresql-dev \
	libxml2-dev \
	libxslt-dev \
	libmemcached-dev \
	cyrus-sasl-dev

#Pillow build process looks for libz.so in /usr/lib
RUN ln -s /lib/libz.so /usr/lib/

RUN pip install -r requirements.txt

RUN python manage.py migrate

RUN npm install
RUN node_modules/.bin/bower install --allow-root

ENV DJANGO_DEBUG=true
ENV PORT=8080

EXPOSE 8080

CMD gunicorn foundation.wsgi:application
