from rest_framework import routers
from django.urls import include, path

from . import api

router = routers.DefaultRouter()

router.register('companies',api.CompanyAPIView,basename="company-list")
router.register('send-aplication-compancy',api.CompanyApplicationAPIView,basename="send-application")
router.register('about-companies',api.AboutCompanyAPIView,basename="about-companies")
urlpatterns=[
    path('',include(router.urls)),
    path('my-company/', api.MyCompanyAPIView.as_view({
    'get': 'get',
    'post': 'post',
    'put': 'put',
    'patch': 'patch',
    }), 
    name='my-company'),
]
