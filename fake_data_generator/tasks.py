import string

from .models import Bot
from django.utils.crypto import get_random_string

from celery import shared_task


@shared_task
def create_bot(total):
    for _ in range(total):
        email = f'{get_random_string(31, string.ascii_letters)}@gmail.com'
        password = get_random_string(50)
        Bot.objects.create(email=email, password=password)
    return f'{total} random bots created'
