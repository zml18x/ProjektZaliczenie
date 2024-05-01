from django.contrib import admin
from django.urls import path
from django.urls import path
from .views import CurrentCurrencyRatesAPIView, SpecificDateCurrencyRatesAPIView, DateRangeCurrencyRatesAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('currency-rates/current/', CurrentCurrencyRatesAPIView.as_view(), name='current_currency_rates'),
    path('currency-rates/date/<str:date>/', SpecificDateCurrencyRatesAPIView.as_view(), name='specific_date_currency_rates'),
    path('currency-rates/range/<str:startDate>/<str:endDate>/', DateRangeCurrencyRatesAPIView.as_view(), name='range_currency_rates'),
]
