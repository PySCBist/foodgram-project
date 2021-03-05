FROM python:3.7.6-slim-buster

RUN apt-get update \
   && apt-get -y install build-essential \
   libpq-dev libssl-dev libffi-dev \
   libxml2-dev libxslt1-dev libssl1.1 \
   postgresql-client

WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown root /entrypoint.sh
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
ENTRYPOINT ["/entrypoint.sh"]
