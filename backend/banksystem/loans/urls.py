from django.urls import path
from .views import LoanViewSet, LoanOptionViewSet, view_customer_loans
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('loans', LoanViewSet, basename='loans')
router.register('loan-options', LoanOptionViewSet, basename='loan_options')

urlpatterns = router.urls + [
    path('customer/<int:id>/', view_customer_loans, name='view_customer_loans')
]
