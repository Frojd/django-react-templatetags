FROM python:3.8-slim
MAINTAINER Frojd

ENV PYTHONUNBUFFERED=1 \
    REQUIREMENTS=requirements.txt

RUN apt-get update \
    && apt-get install -y netcat gcc libpq-dev \
    && apt-get install -y binutils libproj-dev \
    && apt-get install -y gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD . /app/

RUN pip install --upgrade pip \
    && pip install -r $REQUIREMENTS --no-cache-dir

EXPOSE 8080

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["runserver"]
