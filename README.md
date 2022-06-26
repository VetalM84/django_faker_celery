Deployed on Heroku https://django-celery-faker.herokuapp.com/

A learning project with Django + Faker + Celery + RabbitMQ (CloudAMQP Broker).

Manual to start services:
#### Celery on Windows
To run on Windows, run celery with the command below:

`celery -A django-celery-faker worker -l info -P threads`

or

`celery -A django-celery-faker beat -l info -pool==solo`

#### Celery and Beat on Windows
To run on Windows, run celery and beat in two separate command windows with the commands below:

`celery -A django-celery-faker worker -l info -P threads`- celery

`celery -A django-celery-faker beat --scheduler django -l info` - beat

#### Celery on Linux, Mac

`celery -A django-celery-faker worker -l info`

#### Celery and Beat on Linux, Mac

`celery -A django-celery-faker worker --beat --scheduler django -l info`
