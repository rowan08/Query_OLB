FROM python:3.6-slim

WORKDIR /app/query_api
ADD . /app

RUN apt-get update && apt-get -y install supervisor
RUN pip3 install --trusted-host pypi.python.org pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY supervisord.conf /etc/supervisor/supervisord.conf

EXPOSE 8000

ENTRYPOINT  ["/usr/bin/supervisord"]



