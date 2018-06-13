FROM python:2.7
MAINTAINER Open Knowledge International

WORKDIR /app

ENV PORT 80

EXPOSE $PORT
CMD ["echo", "test"]
