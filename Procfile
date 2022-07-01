web: gunicorn django_faker_celery.wsgi --pool=solo --log-file -
worker: celery -A django_faker_celery worker -l info
