from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404

from rest_registration.utils.responses import get_ok_response

from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet,GenericViewSet
from rest_framework import permissions,mixins
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.companies.permissions import IsCompanyPermission
from api.permissions import IsOwnerOrReadOnly
from apps.users.models import User
from apps.channels.services import ChekPopularItem

from .serializers import (
    ItemModel,ItemModelCretaeSerializer,
    ItemImages,ItemModelImageSerailizer,
    Item,ItemCreateSerializer,ItemDetailSerializer,
    MyItemDetailSerializer,
    Color,ColorSerializer,
    Currency,CurrencySerializer,
    ItemCategory,ItemCategorySerializer,
    ItemSubCategory,ItemSubcategorySerializer,
    ItemPayment,ItemPaymentSerializer,
    FavoriteItems,FavoriteItemsSerializer,
    ItemReviews,ItemReviewsSerializer,
    ItemReviewsListSerializer
)
from .filters import ItemSubCategoryFilter,ItemReviewFilter,ItemFilter,FavoriteItemsFilter
from .permissions import IsCompanyUser,ItemPaymentPermissions

class ItemModelAPIView(ModelViewSet):
    queryset = ItemModel.objects.all()
    serializer_class = ItemModelCretaeSerializer
    permission_classes = [permissions.IsAuthenticated,IsCompanyUser]
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(item__company__owner=self.request.user) 
        return queryset

    

class ItemAPIView(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemCreateSerializer
    filterset_class = ItemFilter

    def get_serializer_class(self):
        user:User = self.request.user

        if self.action == 'retrieve':
            if self.get_object().company.owner==user:
                return ItemDetailSerializer
            return ItemDetailSerializer
        
        return self.serializer_class
    
    def get_object(self):
        object:Item = super().get_object()
        
        ip:str = self.request.META.get('REMOTE_ADDR')
        
        user:User = self.request.user if self.request.user.is_authenticated else None 
        
        object.increment_views(user,ip)

        return super().get_object()


class MyItemAPIView(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemCreateSerializer
    permission_class = (permissions.IsAuthenticated,IsCompanyUser)
    filterset_class = ItemFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MyItemDetailSerializer
        return self.serializer_class
    
    def get_queryset(self):
        queryset = super(MyItemAPIView, self).get_queryset()

        user: User = self.request.user
        if user.is_authenticated:

            queryset = queryset.filter(company__owner=self.request.user) 
            return queryset


class ColorAPIView(ReadOnlyModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer    


class CurrencyAPIView(ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer    


class ItemCategoryAPIView(ReadOnlyModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer            


class ItemSubCategoryAPIView(ReadOnlyModelViewSet):
    queryset = ItemSubCategory.objects.all()
    serializer_class = ItemSubcategorySerializer 
    filterset_class = ItemSubCategoryFilter  


class FavoriteItemsAPIView(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    queryset = FavoriteItems.objects.all()
    serializer_class = FavoriteItemsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = FavoriteItemsFilter

    
    def get_queryset(self):
        queryset = super(FavoriteItemsAPIView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user) 
        return queryset


class ItemPaymentAPIView(ModelViewSet):
    queryset = ItemPayment.objects.all()
    serializer_class = ItemPaymentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,ItemPaymentPermissions)

    def get_queryset(self):
        queryset = super(ItemPaymentAPIView, self).get_queryset()
        queryset = queryset.filter(item__company__owner=self.request.user) 
        return queryset
        


class MyReviewsAPIView(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    queryset = ItemReviews.objects.all()
    serializer_class = ItemReviewsSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    filterset_class = ItemReviewFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return ItemReviewsSerializer

        elif self.action == "list":
            return ItemReviewsListSerializer
        
        else:
            return self.serializer_class    
    
    def get_queryset(self):
        user:User = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        return queryset


class MyCompanyReviewsAPIView(ReadOnlyModelViewSet):
    queryset = ItemReviews.objects.all()
    serializer_class = ItemReviewsListSerializer
    permission_classes = (permissions.IsAuthenticated,IsCompanyPermission)

    def get_queryset(self):
        user:User = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(company=user.company)



class ItemReviewsAPIView(ReadOnlyModelViewSet):
    queryset = ItemReviews.objects.all()
    serializer_class = ItemReviewsListSerializer
    filterset_class = ItemReviewFilter