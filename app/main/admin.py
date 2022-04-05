from django.contrib import admin
from main.models import *


class TickerAdmin(admin.ModelAdmin):
    model = Ticker
    list_display = (
        'id', 'name', 'price'
    )


class OperationAdmin(admin.ModelAdmin):
    model = Operation
    list_display = (
        'ticker', 'movement', 'result'
    )


admin.site.register(Ticker, TickerAdmin)
admin.site.register(Operation, OperationAdmin)
