Deployed on Heroku https://django-celery-faker.herokuapp.com/

A learning project with Django + Faker + Celery + RabbitMQ (CloudAMQP Broker).
Due to read-only file system on Heroku, files are not saved to disk.

Manual to start services:
#### Celery on Windows
To run on Windows, run celery with the command below:

`celery -A django_faker_celery worker -l info -P threads`

or

`celery -A django_faker_celery beat -l info -pool==solo`

#### Celery and Beat on Windows
To run on Windows, run celery and beat in two separate command windows with the commands below:

`celery -A django_faker_celery worker -l info -P threads`- celery

`celery -A django_faker_celery beat --scheduler django -l info` - beat

#### Celery on Linux, Mac

`celery -A django_faker_celery worker -l info`

#### Celery and Beat on Linux, Mac

`celery -A django_faker_celery worker --beat --scheduler django -l info`
