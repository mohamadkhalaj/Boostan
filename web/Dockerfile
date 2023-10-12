FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST redis
ENV DJANGO_SETTINGS_MODULE "config.settings.production"
ENV DJANGO_SECRET_KEY ""
ENV WEB_CONCURRENCY 4
ENV REDIS_URL "redis"
ENV DATABASE_URL "postgres://postgres:postgres@db:5432/postgres"
ENV REDIS_SASL_USERNAME ""
ENV REDIS_SASL_PASSWORD ""
ENV PYTHONHASHSEED random
ENV DJANGO_DEBUG False
ENV DJANGO_ADMIN_URL "admin"
ENV DJANGO_ALLOWED_HOSTS "localhost,127.0.0.1"
ENV DJANGO_ACCOUNT_ALLOW_REGISTRATION False
ENV SENTRY_DSN ""
RUN mkdir /web
RUN touch /web/requirements.txt
RUN echo "-r requirements/production.txt" >> /web/requirements.txt
COPY ./requirements /web/requirements

WORKDIR /web

RUN pip install --upgrade pip
RUN pip install -r requirements.txt