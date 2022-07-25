# Boostan

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![.github/workflows/prod.yml](https://github.com/mohamadkhalaj/Boostan/actions/workflows/prod.yml/badge.svg)](https://github.com/mohamadkhalaj/Boostan/actions/workflows/prod.yml)

## Features✨
### Users
- Beautiful and responsive design
- Get food list, Reserved list, Credit amount, Reserve food and Get forget code from boostan
- Change theme based on user telegram theme settings
- Supports multi sessions and user is always logged in
- Session manager and devices info
### Admins
- Enable/Disable requests logging
- Set rate limit
- Different operating modes such: Block, Whitelist and normal mode
- Telegram alert settings
- Change any alerts and error messages from admin panel
- Multi language support see [locale](https://github.com/mohamadkhalaj/Boostan/tree/master/locale)
- Some statistics

## Tech
We used several frameworks and services for doing our job so well:

- [Django]() - We used django for our backend
- [Redis]() - Datebase memory caching
- [PostgreSql]() - Sql datebase
- [Telegram web-app-bot]() - Better user experient
- [JavaScript]() - Our frontEnd made with pure js
- [jQuery]() - FrontEnd
- [Twitter Bootstrap]() - Great UI boilerplate for modern and responsive web apps
- [Heroku]() - Deployment
- [Sentry]() - Error tracking for both Django/JS
- [Google analytics]() - For users analysis

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Github workflows (CI/CD)

If you want to pass ci/cd and auto deploy after each commit, you should add below secrets to your github repo secret lists.
Instructions on how to use them in your own application are linked below.

[Github secret instructions](https://github.com/Azure/actions-workflow-samples/blob/master/assets/create-secrets-for-GitHub-workflows.md)
| KEY | VALUE |
| ------ | ------ |
| BOOSTAN_USERNAME | Boostan username (for testing) (optional)|
| BOOSTAN_PASSWORD | Boostan password (for testing) (optional)|
| HEROKU_API_KEY | Your heroku API_KEY |
| HEROKU_APP_NAME | Your heroku app name |
| HEROKU_EMAIL | Your heroku account email |


## Basic Commands

### Installation (normal)

Install the dependencies and devDependencies and start the server.

```sh
$ pip install -r requirements/local.txt
$ python manage.py migrate
$ python manage.py loaddefaults
$ python manage.py runserver
```

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

## Debug your app with telegram desktop

You should install telegram beta and enable inspect element in experimental setitngs more detail [Telegram doc](https://core.telegram.org/bots/webapps#debug-mode-for-web-apps).

We should use HTTPS for debugging our app with telegram, so we have to make and install our own certificates.
So we should install MkCert (See detail [Mkcert repo](https://github.com/FiloSottile/mkcert)).

Now create the certificates with this command:
```sh
$ mkcert -cert-file cert.pem -key-file key.pem 0.0.0.0 localhost 127.0.0.1 ::1
```
Replace 0.0.0.0, localhost, 127.0.0.1 with the domains you’ll be running locally.

cert.pem and key.pem files will be created in your current working directory. you can replace them whichever names you wish.

but since we shall be running them in Django, copy them to the same folder as manage.py

Run below command to add certificates to browser trusted certificates list.
```
$ mkcert -install
```
Then you can run project with this command:
```
$ python manage.py runsslserver — certificate cert.pem — key key.pem
```

### Type checks

Running type checks with mypy:

    $ mypy boostan

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests
**(optional)** If you wanna test with credentials and cover more code testing, you can set your username and password in env variables.
```
$ export BOOSTAN_USERNAME="YOUR_USERNAME"
$ export BOOSTAN_PASSWORD="YOUR_PASSWORD"
```

    $ python manage.py test api

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Environment variables (Production only)

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
| REDIS_URL | Your redis url (for memcache) (free redis sever [redis cloud](https://app.redislabs.com/#/login)) |
| REDIS_SASL_PASSWORD | Redis SASL password |
| REDIS_SASL_USERNAME | Redis SASL username |
| SENTRY_DSN | Your sentry error tracker DSN code (See detail [sentry django doc](https://docs.sentry.io/platforms/python/guides/django/)) |

### Heroku
**Click below button for easy deploy to heroku!**

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/mohamadkhalaj/Boostan/tree/master/)

## License

GPL-3.0 license

**Free Software, Hell Yeah!**

## Screenshots
#### Dynamic theme (Telegram)
![menu](https://user-images.githubusercontent.com/62938359/180774724-312a2754-1bca-453f-873d-8584042f00f8.gif)
![reserve](https://user-images.githubusercontent.com/62938359/180774810-bc2923cc-229e-441f-80df-6bba1fef2b9a.gif)

#### Desktop version
![1](https://user-images.githubusercontent.com/62938359/180776746-edcbc2e5-eb97-455c-8628-65208998cde7.png)
![8](https://user-images.githubusercontent.com/62938359/180776756-b7d2e79e-098f-4066-976c-adcfc40453a2.png)
![2](https://user-images.githubusercontent.com/62938359/180774771-7e2511bc-59af-422d-81f9-d719491409aa.png)
![4](https://user-images.githubusercontent.com/62938359/180774779-8cb04003-b0be-46cf-a12b-e8df5de05874.png)
![5](https://user-images.githubusercontent.com/62938359/180774785-7ba64547-e6f9-4807-bead-7f06854f5bc3.png)
![7](https://user-images.githubusercontent.com/62938359/180774801-83c8cbb8-9f64-437a-9d6f-f6c02f885a43.png)
