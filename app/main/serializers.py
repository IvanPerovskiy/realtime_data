from rest_framework import serializers

from main.models import Ticker


class TickerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticker
        fields = ('id', 'name', 'price')


class TickerHistorySerializer(serializers.ModelSerializer):
    history = serializers.ListField(child=serializers.ListField(child=serializers.IntegerField()))

    class Meta:
        model = Ticker
        fields = ('id', 'name', 'price', 'history')











