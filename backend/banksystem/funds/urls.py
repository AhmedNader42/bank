from django.urls import path
from .views import FundViewSet, FundOptionViewSet, view_funder_funds, view_pending_funds, verify_fund_payment
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('funds', FundViewSet, basename='funds')
router.register('fund-options', FundOptionViewSet, basename='fund_options')

urlpatterns = router.urls + [
    path('funder/<int:id>/', view_funder_funds, name='view_funder_funds'),
    path('funds-pending/', view_pending_funds, name='view_pending_funds'),
    path('verify-fund/<int:fund_id>/',
         verify_fund_payment, name='verify_fund_payment')
]
