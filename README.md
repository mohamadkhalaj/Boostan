# boostan

reserve food from boostan website.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![.github/workflows/prod.yml](https://github.com/mohamadkhalaj/Boostan/actions/workflows/prod.yml/badge.svg)](https://github.com/mohamadkhalaj/Boostan/actions/workflows/prod.yml)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Environment variables (Production)

See detailed [django Heroku](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).
Instructions on how to use them in your own application are linked below.

| KEY | VALUE |
| ------ | ------ |
| DJANGO_SECRET_KEY | ```$(openssl rand -base64 64)``` |
| WEB_CONCURRENCY | 4 |
| DJANGO_DEBUG | False |
| DJANGO_SETTINGS_MODULE | config.settings.production |
| PYTHONHASHSEED | random |
| DJANGO_ADMIN_URL | RANDOM_STRING/ |
| DJANGO_ALLOWED_HOSTS | YOUR_DOMAIN |
| DJANGO_ACCOUNT_ALLOW_REGISTRATION | False |
| REDIS_URL | Your redis url (for memcache) (free redis sever [redis cloud](https://app.redislabs.com/#/login) |
| REDIS_SASL_PASSWORD | Redis SASL password |
| REDIS_SASL_USERNAME | Redis SASL username |
| SENTRY_DSN | Your sentry error tracker DSN code (See detail [sentry django doc](https://docs.sentry.io/platforms/python/guides/django/)) |

## Github workflows (CI/CD)

If you want to pass ci/cd and auto deploy after each commit, you should add below secrets to your github repo secret lists.
Instructions on how to use them in your own application are linked below.

| KEY | VALUE |
| ------ | ------ |
| BOOSTAN_USERNAME | Boostan username (for testing) (optional)|
| BOOSTAN_PASSWORD | Boostan password (for testing) (optional)|
| HEROKU_API_KEY | Your heroku API_KEY |
| HEROKU_APP_NAME | Your heroku app name |
| HEROKU_EMAIL | Your heroku account email |


## Basic Commands

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy boostan

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ python manage.py test api

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Heroku
- [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/mohamadkhalaj/Boostan/tree/master/)
- See detailed [cookiecutter-django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).
