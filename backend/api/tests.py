from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from .models import Currency, CurrencyRate
from .views import GetSpecificDateCurrencyRatesFromNbp, GetSpecificDateRangeCurrencyRatesFromNbp, isWeekday

class TestCurrencyRatesAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        CurrencyRate.objects.all().delete()
        Currency.objects.all().delete()
        self.currency_usd = Currency.objects.create(code='USD', name='US Dollar')
        self.currency_eur = Currency.objects.create(code='EUR', name='Euro')
        self.current_date = datetime.now().date()
        self.weekend_date = self.current_date - timedelta(days=(self.current_date.weekday() + 2) % 7 + 1)
        self.start_date = (self.current_date - timedelta(days=2)).strftime('%Y-%m-%d')
        self.end_date = (self.current_date - timedelta(days=1)).strftime('%Y-%m-%d')

    def test_isWeekday(self):
        self.assertTrue(isWeekday(datetime(2024, 6, 3)))
        self.assertFalse(isWeekday(datetime(2024, 6, 2)))

    @patch('requests.get')
    @patch('api.models.Currency.objects.get_or_create')
    @patch('api.models.CurrencyRate.objects.create')
    def test_GetSpecificDateCurrencyRatesFromNbp(self, mockCreate, mockGetOrCreate, mockRequestsGet):
        sampleResponse = [{
            "table": "A",
            "no": "001/A/NBP/2021",
            "effectiveDate": "2021-01-04",
            "rates": [
                {"currency": "bat (Tajlandia)", "code": "THB", "mid": 0.1234},
                {"currency": "dolar amerykański", "code": "USD", "mid": 3.6789},
                {"currency": "euro", "code": "EUR", "mid": 4.5678}
            ]
        }]
        
        mockRequestsGet.return_value = Mock(status_code=200, json=lambda: sampleResponse)

        mock_thb = Currency(code='THB', name='bat (Tajlandia)')
        mock_usd = Currency(code='USD', name='dolar amerykański')
        mock_eur = Currency(code='EUR', name='euro')
        
        mockGetOrCreate.side_effect = [
            (mock_thb, True),
            (mock_usd, True),
            (mock_eur, True)
        ]

        GetSpecificDateCurrencyRatesFromNbp('2021-01-04')

        mockRequestsGet.assert_called_once_with('http://api.nbp.pl/api/exchangerates/tables/A/2021-01-04')

        self.assertEqual(mockGetOrCreate.call_count, 3)
        mockGetOrCreate.assert_any_call(code='THB', defaults={'name': 'bat (Tajlandia)'})
        mockGetOrCreate.assert_any_call(code='USD', defaults={'name': 'dolar amerykański'})
        mockGetOrCreate.assert_any_call(code='EUR', defaults={'name': 'euro'})

        self.assertEqual(mockCreate.call_count, 3)
        mockCreate.assert_any_call(currency=mock_thb, rate_date='2021-01-04', rate=0.1234)
        mockCreate.assert_any_call(currency=mock_usd, rate_date='2021-01-04', rate=3.6789)
        mockCreate.assert_any_call(currency=mock_eur, rate_date='2021-01-04', rate=4.5678)

    @patch('requests.get')
    @patch('api.models.Currency.objects.get_or_create')
    @patch('api.models.CurrencyRate.objects.create')
    def test_GetSpecificDateRangeCurrencyRatesFromNbp(self, mockCreate, mockGetOrCreate, mockRequestsGet):
        sample_response = [
            {
                "table": "A",
                "no": "001/A/NBP/2021",
                "effectiveDate": "2021-01-04",
                "rates": [
                    {"currency": "bat (Tajlandia)", "code": "THB", "mid": 0.1234},
                    {"currency": "dolar amerykański", "code": "USD", "mid": 3.6789},
                    {"currency": "euro", "code": "EUR", "mid": 4.5678}
                ]
            },
            {
                "table": "A",
                "no": "002/A/NBP/2021",
                "effectiveDate": "2021-01-05",
                "rates": [
                    {"currency": "bat (Tajlandia)", "code": "THB", "mid": 0.1240},
                    {"currency": "dolar amerykański", "code": "USD", "mid": 3.6800},
                    {"currency": "euro", "code": "EUR", "mid": 4.5700}
                ]
            }
        ]
        
        mockRequestsGet.return_value = Mock(status_code=200, json=lambda: sample_response)

        mock_thb = Mock(spec=Currency, code='THB', name='bat (Tajlandia)')
        mock_usd = Mock(spec=Currency, code='USD', name='dolar amerykański')
        mock_eur = Mock(spec=Currency, code='EUR', name='euro')
        
        mockGetOrCreate.side_effect = [
            (mock_thb, True),
            (mock_usd, True),
            (mock_eur, True),
            (mock_thb, True),
            (mock_usd, True),
            (mock_eur, True)
        ]

        GetSpecificDateRangeCurrencyRatesFromNbp('2021-01-04', '2021-01-05')

        mockRequestsGet.assert_called_once_with('http://api.nbp.pl/api/exchangerates/tables/A/2021-01-04/2021-01-05')

        self.assertEqual(mockGetOrCreate.call_count, 6)
        mockGetOrCreate.assert_any_call(code='THB', defaults={'name': 'bat (Tajlandia)'})
        mockGetOrCreate.assert_any_call(code='USD', defaults={'name': 'dolar amerykański'})
        mockGetOrCreate.assert_any_call(code='EUR', defaults={'name': 'euro'})

        self.assertEqual(mockCreate.call_count, 6)
        mockCreate.assert_any_call(currency=mock_thb, rate_date=datetime.strptime('2021-01-04', '%Y-%m-%d').date(), rate=0.1234)
        mockCreate.assert_any_call(currency=mock_usd, rate_date=datetime.strptime('2021-01-04', '%Y-%m-%d').date(), rate=3.6789)
        mockCreate.assert_any_call(currency=mock_eur, rate_date=datetime.strptime('2021-01-04', '%Y-%m-%d').date(), rate=4.5678)
        mockCreate.assert_any_call(currency=mock_thb, rate_date=datetime.strptime('2021-01-05', '%Y-%m-%d').date(), rate=0.1240)
        mockCreate.assert_any_call(currency=mock_usd, rate_date=datetime.strptime('2021-01-05', '%Y-%m-%d').date(), rate=3.6800)
        mockCreate.assert_any_call(currency=mock_eur, rate_date=datetime.strptime('2021-01-05', '%Y-%m-%d').date(), rate=4.5700)

    @patch('api.views.GetSpecificDateCurrencyRatesFromNbp')
    @patch('api.views.isWeekday', return_value=True)
    def test_currentCurrencyRatesApi(self, mock_isWeekday, mock_GetSpecificDateCurrencyRatesFromNbp):
        url = reverse('current_currency_rates')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('api.views.GetSpecificDateCurrencyRatesFromNbp')
    @patch('api.views.isWeekday', return_value=True)
    def test_specificDateCurrencyRatesApi(self, mock_isWeekday, mock_GetSpecificDateCurrencyRatesFromNbp):
        date = self.current_date.strftime('%Y-%m-%d')
        url = reverse('specific_date_currency_rates', args=[date])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('api.views.GetSpecificDateRangeCurrencyRatesFromNbp')
    def test_dateRangeCurrencyRatesApi(self, mock_GetSpecificDateRangeCurrencyRatesFromNbp):
        url = reverse('range_currency_rates', args=[self.start_date, self.end_date])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('api.views.isWeekday', return_value=True)
    def test_currentCurrencyRatesWithExistingData(self, mock_isWeekday):
        CurrencyRate.objects.create(currency=self.currency_usd, rate_date=self.current_date, rate=3.75)
        CurrencyRate.objects.create(currency=self.currency_eur, rate_date=self.current_date, rate=4.20)

        url = reverse('current_currency_rates')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @patch('api.views.isWeekday', return_value=True)
    @patch('api.views.GetSpecificDateCurrencyRatesFromNbp')
    def test_currentCurrencyRatesWithoutExistingData(self, mock_GetSpecificDateCurrencyRatesFromNbp, mock_isWeekday):
        url = reverse('current_currency_rates')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_GetSpecificDateCurrencyRatesFromNbp.assert_called_once_with(self.current_date)

    @patch('api.views.isWeekday', return_value=False)
    def test_currentCurrencyRatesOnWeekend(self, mock_isWeekday):
        url = reverse('current_currency_rates')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    @patch('api.views.isWeekday', return_value=True)
    def test_specificDateCurrencyRatesWithExistingData(self, mock_isWeekday):
        CurrencyRate.objects.create(currency=self.currency_usd, rate_date=self.current_date, rate=3.75)
        CurrencyRate.objects.create(currency=self.currency_eur, rate_date=self.current_date, rate=4.20)

        date = self.current_date.strftime('%Y-%m-%d')
        url = reverse('specific_date_currency_rates', args=[date])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @patch('api.views.isWeekday', return_value=True)
    @patch('api.views.GetSpecificDateCurrencyRatesFromNbp')
    def test_specificDateCurrencyRatesWithoutExistingData(self, mock_GetSpecificDateCurrencyRatesFromNbp, mock_isWeekday):
        date = self.current_date.strftime('%Y-%m-%d')
        url = reverse('specific_date_currency_rates', args=[date])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_GetSpecificDateCurrencyRatesFromNbp.assert_called_once_with(datetime.strptime(date, '%Y-%m-%d').date())

    @patch('api.views.isWeekday', return_value=False)
    def test_specificDateCurrencyRatesOnWeekend(self, mock_isWeekday):
        date = self.weekend_date.strftime('%Y-%m-%d')
        url = reverse('specific_date_currency_rates', args=[date])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    @patch('api.views.GetSpecificDateRangeCurrencyRatesFromNbp')
    def test_dateRangeCurrencyRatesWithExistingData(self, mock_GetSpecificDateRangeCurrencyRatesFromNbp):
        CurrencyRate.objects.create(currency=self.currency_usd, rate_date=datetime.strptime(self.start_date, '%Y-%m-%d').date(), rate=3.75)
        CurrencyRate.objects.create(currency=self.currency_eur, rate_date=datetime.strptime(self.end_date, '%Y-%m-%d').date(), rate=4.20)

        url = reverse('range_currency_rates', args=[self.start_date, self.end_date])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @patch('api.views.GetSpecificDateRangeCurrencyRatesFromNbp')
    def test_dateRangeCurrencyRatesWithoutExistingData(self, mock_GetSpecificDateRangeCurrencyRatesFromNbp):
        url = reverse('range_currency_rates', args=[self.start_date, self.end_date])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_GetSpecificDateRangeCurrencyRatesFromNbp.assert_called_once_with(datetime.strptime(self.start_date, '%Y-%m-%d').date(), datetime.strptime(self.end_date, '%Y-%m-%d').date())

    @patch('api.views.GetSpecificDateRangeCurrencyRatesFromNbp')
    def test_dateRangeCurrencyRatesWithPartialExistingData(self, mock_GetSpecificDateRangeCurrencyRatesFromNbp):
        CurrencyRate.objects.create(currency=self.currency_usd, rate_date=datetime.strptime(self.start_date, '%Y-%m-%d').date(), rate=3.75)

        url = reverse('range_currency_rates', args=[self.start_date, self.end_date])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        mock_GetSpecificDateRangeCurrencyRatesFromNbp.assert_called_once_with(datetime.strptime(self.start_date, '%Y-%m-%d').date(), datetime.strptime(self.end_date, '%Y-%m-%d').date())

    @patch('api.views.GetSpecificDateRangeCurrencyRatesFromNbp')
    def test_dateRangeCurrencyRatesWithWeekends(self, mock_GetSpecificDateRangeCurrencyRatesFromNbp):
        weekend_start_date = self.weekend_date.strftime('%Y-%m-%d')
        weekend_end_date = (self.weekend_date + timedelta(days=1)).strftime('%Y-%m-%d')

        url = reverse('range_currency_rates', args=[weekend_start_date, weekend_end_date])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_GetSpecificDateRangeCurrencyRatesFromNbp.assert_called_once_with(datetime.strptime(weekend_start_date, '%Y-%m-%d').date(), datetime.strptime(weekend_end_date, '%Y-%m-%d').date())
