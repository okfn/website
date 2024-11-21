FROM python:3.10-buster
MAINTAINER Open Knowledge Foundation

WORKDIR /app
RUN apt-get update -y && apt-get upgrade -y
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
RUN apt-get install -y nginx
RUN apt-get install -y supervisor

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
COPY deployment/nginx.conf /etc/nginx/conf.d/default.conf
COPY deployment/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY deployment/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

COPY docs ./docs
COPY foundation ./foundation
COPY .env.base ./.env.base
COPY lib ./lib
COPY sendemail ./sendemail
COPY static ./static
COPY templates ./templates
COPY manage.py .
COPY package-lock.json .
COPY package.json .
COPY requirements.txt .
COPY deployment/gunicorn.config.py .

RUN pip install -r requirements.txt
RUN . /root/.nvm/nvm.sh && nvm install 16
RUN . /root/.nvm/nvm.sh && nvm use 16

ENV PORT 80
EXPOSE $PORT

COPY docker-entrypoint.d /docker-entrypoint.d
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
