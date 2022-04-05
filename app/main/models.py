from django.db import models


class Ticker(models.Model):
    name = models.CharField(max_length=200)
    price = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['name']

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Operation(models.Model):
    ticker = models.ForeignKey(Ticker, related_name='operations', on_delete=models.PROTECT)
    movement = models.IntegerField(choices=((1, 'Positive'), (-1, 'Negative')))
    result = models.BigIntegerField()

    created = models.DateTimeField(auto_now_add=True)
