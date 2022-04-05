from random import random

from django.conf import settings
from django.contrib.auth import get_user_model

from main.models import Ticker


def generate_movement(step: int):
    movement = -step if random() < 0.5 else step
    return movement


def get_or_create_superuser():
    superuser = get_user_model().objects.filter(
        is_superuser=True
    ).first()
    if not superuser:
        get_user_model().objects.create_superuser(
            username=settings.SUPERUSER_NAME,
            password=settings.SUPERUSER_PASSWORD
        )


def generate_tickers():
    tickers = Ticker.objects.all()
    if len(tickers) == 0:
        objs = []
        for i in range(int(settings.COUNT)):
            objs.append(Ticker(name=f'ticker_{str(i).zfill(2)}'))
        Ticker.objects.bulk_create(objs)


def start_service():
    """
    Вызывается при сборке проекта
    """
    get_or_create_superuser()
    generate_tickers()

