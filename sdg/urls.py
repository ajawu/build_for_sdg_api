from django.conf.urls import url
from .views import EstimatorView, LogView

urlpatterns = [
    url(r'on-covid-19/logs', LogView.as_view(), name='log_view'),
    url(r'on-covid-19/([\w]+)$', EstimatorView.as_view(), name='estimator_view'),
    url(r'on-covid-19/', EstimatorView.as_view(), name='estimator_view'),
]

