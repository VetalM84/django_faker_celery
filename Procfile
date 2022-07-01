web: gunicorn django_faker_celery.wsgi --log-file -
worker: celery -A django_faker_celery worker -l info
