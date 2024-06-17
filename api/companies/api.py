from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime

from rest_registration.utils.responses import get_ok_response
from rest_registration.api.serializers import DefaultUserProfileSerializer
from rest_registration.api.views.base import BaseAPIView 

from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import GenericViewSet,ModelViewSet,ReadOnlyModelViewSet,ViewSet
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import mixins

from .serializers import (
    CompanySerializer,Company,
    CompanyApplicationSerializer,CompanyApplication,
    MyCompanySerializer,AboutCompanySerializer
    )
from .permissions import IsCompanyPermission



class CompanyAPIView(ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer



class CompanyApplicationAPIView(
    mixins.CreateModelMixin,
    GenericViewSet
    ):
    queryset = CompanyApplication.objects.all()
    serializer_class = CompanyApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)



class MyCompanyAPIView(ViewSet,BaseAPIView):
    permission_classes = [permissions.IsAuthenticated,IsCompanyPermission]
    serializer_class = MyCompanySerializer
    
    def get(self, request:Request):
        serializer = self.get_serializer(request.user.company)
        return Response(serializer.data)

    def post(self, request):
        return self._update_company(request)

    def put(self, request):
        return self._update_company(request)

    def patch(self, request):
        return self._update_company(request, partial=True)

    def _update_company(self, request, partial=False):
        company_instance = request.user.company
        serializer = self.get_serializer(instance=company_instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AboutCompanyAPIView(ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = AboutCompanySerializer

