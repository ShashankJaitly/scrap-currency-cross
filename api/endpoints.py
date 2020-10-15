from .views import ListCurrencyView
from django.urls import path

urlpatterns = [
    path('', ListCurrencyView.as_view())
]
