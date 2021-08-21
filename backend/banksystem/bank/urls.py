from django.urls import path
from .views import get_total_amount, system_report


urlpatterns = [
    path('bank-balance/', get_total_amount, name='get_total_amount'),
    path('system-report/', system_report, name='system_report'),
]
