from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from main.models import Ticker
from main.responses import *
from main.serializers import TickerSerializer, TickerHistorySerializer


class TickerViewSet(viewsets.GenericViewSet):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'name']
    ordering_fields = ['id', 'created', 'name']
    ordering = ['id']
    history_response = openapi.Response(SUCCESS_RESPONSE, TickerHistorySerializer)

    def list(self, request, *args, **kwargs):
        """
        Список всех инструментов
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={
        200: history_response,
        404: NOT_FOUND
    }, manual_parameters=[
        openapi.Parameter(
            'start',
            openapi.IN_QUERY,
            description="Точка отсчета истории изменений",
            type=openapi.TYPE_NUMBER,
            required=False
        )
    ])
    def retrieve(self, request, *args, **kwargs):
        """
        Стоимость инструмента с историей изменений.
        С помощью параметра start можно получить историю изменений с заданного времени.
        """
        instance = self.get_object()
        data = self.get_serializer(instance=instance).data

        history = [(0, 0)]
        history.extend(enumerate(instance.operations.values_list('result', flat=True), 1))
        start = request.query_params.get('start', 0)

        data['history'] = history[int(start):]

        return Response(data=data, status=status.HTTP_200_OK)


