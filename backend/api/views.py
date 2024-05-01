from rest_framework import generics
from rest_framework.response import Response
from .models import Currency, CurrencyRate
from datetime import datetime
import requests

def isWeekday(date):
    return date.weekday() < 5

def GetSpecificDateCurrencyRatesFromNbp(date):
    response = requests.get(f'http://api.nbp.pl/api/exchangerates/tables/A/{date}')
    data = response.json()
    
    for item in data[0]['rates']:
        currency, _ = Currency.objects.get_or_create(
            code=item['code'],
            defaults={'name': item['currency']}
        )

        CurrencyRate.objects.create(
            currency=currency,
            rate_date= date,
            rate=item['mid']
        )

def GetSpecificDateRangeCurrencyRatesFromNbp(startDate, endDate):
    response = requests.get(f'http://api.nbp.pl/api/exchangerates/tables/A/{startDate}/{endDate}')
    data = response.json()

    for table in data:
        ratesDate = datetime.strptime(table['effectiveDate'], '%Y-%m-%d').date()
        if not CurrencyRate.objects.filter(rate_date=ratesDate).exists():
            for item in table['rates']:
                currency, _ = Currency.objects.get_or_create(
                    code=item['code'],
                    defaults={'name': item['currency']}
                )

                CurrencyRate.objects.create(
                    currency=currency,
                    rate_date=ratesDate,
                    rate=item['mid']
                )


class CurrentCurrencyRatesAPIView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        currentDate = datetime.now().date()

        if isWeekday(currentDate):
            if not CurrencyRate.objects.filter(rate_date=currentDate):
                GetSpecificDateCurrencyRatesFromNbp(currentDate)

        rates = CurrencyRate.objects.filter(rate_date=currentDate)
        serializedData = [{'currency': rate.currency.name, 'rate': rate.rate, 'date': rate.rate_date} for rate in rates]
        
        return Response(serializedData)

class SpecificDateCurrencyRatesAPIView(generics.RetrieveAPIView):
    def get(self, request, date, *args, **kwargs):
        date = datetime.strptime(date, '%Y-%m-%d').date()

        if isWeekday(date):
            if not CurrencyRate.objects.filter(rate_date=date).exists():
                GetSpecificDateCurrencyRatesFromNbp(date)

        rates = CurrencyRate.objects.filter(rate_date=date)
        serializedData = [{'currency': rate.currency.name, 'rate': rate.rate, 'date': rate.rate_date} for rate in rates]

        return Response(serializedData)

class DateRangeCurrencyRatesAPIView(generics.RetrieveAPIView):
    def get(self, request, startDate, endDate, *args, **kwargs):
        startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
        endDate = datetime.strptime(endDate, '%Y-%m-%d').date()

        GetSpecificDateRangeCurrencyRatesFromNbp(startDate, endDate)

        rates = CurrencyRate.objects.filter(rate_date__range=[startDate, endDate])
        serializedData = [{'currency': rate.currency.name, 'rate': rate.rate, 'date': rate.rate_date} for rate in rates]
        sortedData = sorted(serializedData, key=lambda x: x['date'])

        return Response(sortedData)
