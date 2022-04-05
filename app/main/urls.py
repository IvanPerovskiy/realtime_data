from django.urls import path, include
from rest_framework import routers

from main import views


router = routers.SimpleRouter(trailing_slash=False)
router.register('', views.TickerViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
