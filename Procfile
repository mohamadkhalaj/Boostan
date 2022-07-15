release: python manage.py migrate && python3 manage.py loaddefaults 
web: gunicorn config.wsgi:application
