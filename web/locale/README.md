Translations
============

### Install dependencies

```
$ sudo apt-get install gettext
```

Translations will be placed in this folder when running:

    $ python manage.py makemessages -l <LANG_CODE>

Then use apps like poedit to translate messages.

After that you should run below command to compile messages:

```
$ python manage.py compilemessages
```

**More details: [Django translation doc](https://docs.djangoproject.com/en/4.0/topics/i18n/translation/).**
