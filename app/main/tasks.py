from celery import shared_task
from django.db import transaction
from django.conf import settings

from main.models import Ticker, Operation
from main.utils import generate_movement


@shared_task
def task_every_second():
    """
    Изменяет цены всем торговым инструментам.
    Шаг изменений берется из настроек
    """
    step = int(settings.STEP)
    prices = []
    operation_objs = []
    for ticker in Ticker.objects.all():
        movement = generate_movement(step)
        result = ticker.price + movement
        ticker.price = result
        prices.append(ticker)
        operation_objs.append(Operation(
            ticker_id=ticker.id,
            movement=movement,
            result=result
        ))
    Ticker.objects.bulk_update(prices, ['price'])
    Operation.objects.bulk_create(operation_objs)





