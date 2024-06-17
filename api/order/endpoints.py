from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()

router.register('send-order',api.OrderAPIView)
router.register('my-purchases',api.MyPurchasesAPIView)
router.register('my-orders',api.OrderItemAPIView,basename="my-orders")

urlpatterns = [
    path('', include(router.urls)),
]
