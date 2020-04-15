from django.conf.urls import url
from django.urls import path
from .views import EstimatorView, LogView

urlpatterns = [
    url(r'on-covid-19/([\w]+)/?$', EstimatorView.as_view(), name='estimator_view'),
    path('on-covid-19/', EstimatorView.as_view(), name='estimator_view'),
]
