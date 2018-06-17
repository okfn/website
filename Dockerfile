FROM python:2.7
MAINTAINER Open Knowledge International

WORKDIR /app
RUN apt-get update
RUN apt-get install -y libmemcached-dev

COPY article_list_item ./article_list_item
COPY contrib ./contrib
COPY docs ./docs
COPY foundation ./foundation
COPY lib ./lib
COPY sendemail ./sendemail
COPY static ./static
COPY templates ./templates
COPY tools ./tools
COPY manage.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PORT 80
EXPOSE $PORT

CMD gunicorn foundation.wsgi:application --access-logfile '-' --error-logfile '-'
