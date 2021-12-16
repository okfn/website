FROM python:3.8-buster
MAINTAINER Open Knowledge Foundation

WORKDIR /app
RUN apt-get update
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
RUN apt-get install -y nginx
RUN apt-get install -y supervisor

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
COPY deployment/nginx.conf /etc/nginx/conf.d/default.conf
COPY deployment/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY deployment/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

COPY aldryn_quote ./aldryn_quote
COPY aldryn_video ./aldryn_video
COPY article_list_item ./article_list_item
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
RUN . /root/.nvm/nvm.sh && nvm install 10
RUN . /root/.nvm/nvm.sh && nvm use 10

ENV PORT 80
EXPOSE $PORT

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
