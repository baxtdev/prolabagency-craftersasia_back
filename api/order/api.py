from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404

from rest_registration.utils.responses import get_ok_response

from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet,GenericViewSet
from rest_framework import permissions,mixins
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.permissions import IsCompanyUser
from apps.users.models import User


from .filters import OrderFilter,OrderItemFilter
from .serializers import (
    OrderItemListSerializer, OrderItems,OrderItemSerializer,
    Order,OrderCreateSerializer,OrderListSerializer
)

class MyPurchasesAPIView(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = OrderFilter

    def get_queryset(self):
        user:User = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        return queryset


class OrderAPIView(mixins.CreateModelMixin,GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = OrderFilter


class OrderItemAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemListSerializer
    permission_classes = (permissions.IsAuthenticated,IsCompanyUser)
    filterset_class = OrderItemFilter

    def get_queryset(self):
        user:User = self.request.user
        queryset = super().get_queryset()    
        queryset = queryset.filter(company=user.company)
        return queryset
        