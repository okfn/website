FROM python:2.7
MAINTAINER Open Knowledge International

WORKDIR /app
RUN apt-get update
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash

COPY article_list_item ./article_list_item
COPY contrib ./contrib
COPY docs ./docs
COPY foundation ./foundation
COPY lib ./lib
COPY sendemail ./sendemail
COPY static ./static
COPY templates ./templates
COPY tools ./tools
COPY .bowerrc .
COPY bower.json .
COPY manage.py .
COPY package-lock.json .
COPY package.json .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN . /root/.nvm/nvm.sh && nvm install 10
RUN . /root/.nvm/nvm.sh && nvm use 10
RUN . /root/.nvm/nvm.sh && npm install -g bower
RUN . /root/.nvm/nvm.sh && bower install --allow-root

ENV PORT 80
EXPOSE $PORT

CMD python manage.py migrate && \
    python manage.py update_index && \
    gunicorn foundation.wsgi:application \ 
        --access-logfile '-' \ 
        --error-logfile '-'
