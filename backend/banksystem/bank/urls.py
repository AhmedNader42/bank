from django.urls import path
from .views import get_total_amount


urlpatterns = [
    path('bank-balance/', get_total_amount, name='get_total_amount')
]
