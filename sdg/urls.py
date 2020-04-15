from django.conf.urls import url
from django.urls import path
from .views import EstimatorView, LogView

urlpatterns = [
    path(r'on-covid-19/logs', LogView.as_view(), name='log_view'),
    path(r'on-covid-19/json', EstimatorView.as_view(), name='estimator_view'),
    path(r'on-covid-19/xml', EstimatorView.as_view(), name='estimator_view'),
    path(r'on-covid-19/', EstimatorView.as_view(), name='estimator_view'),
]

