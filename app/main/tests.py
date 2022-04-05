from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from main.models import Ticker, Operation
from main.utils import generate_tickers
from main.tasks import task_every_second


@override_settings(
    BROKER_BACKEND='memory',
    CELERY_TASK_EAGER_PROPAGATES=True,
    CELERY_TASK_ALWAYS_EAGER=True,
    MEDIA_ROOT='/media/media_test/'
)
class RealtimeTestCase(TestCase):
    def setUp(self):
        generate_tickers()

    def test_task(self):
        tickers = Ticker.objects.all()
        self.assertEqual(len(tickers), 100)
        task_every_second()
        task_every_second()
        self.assertEqual(len(Operation.objects.all()), 200)
        ticker = Ticker.objects.get(name='ticker_50')
        operations = ticker.operations.all()
        self.assertEqual(operations[1].result, ticker.price)

    def test_views(self):
        self.user = APIClient()
        response = self.user.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual((len(response.json())), 100)
        self.assertEqual(response.json()[10]['name'], 'ticker_10')



