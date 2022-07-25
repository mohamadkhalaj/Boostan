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
