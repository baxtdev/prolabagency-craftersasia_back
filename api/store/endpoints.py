from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register('items-models',api.ItemModelAPIView)
router.register('items',api.ItemAPIView)
router.register('colors',api.ColorAPIView)
router.register('item-categories',api.ItemCategoryAPIView)
router.register('item-subcategories',api.ItemSubCategoryAPIView)
router.register('currencies',api.CurrencyAPIView)
router.register('favorite-items',api.FavoriteItemsAPIView)
router.register('item-payments',api.ItemPaymentAPIView,basename="items")
router.register('my-items',api.MyItemAPIView,basename="my-items")
router.register('item-reviews',api.ItemReviewsAPIView)
router.register('my-company-reviews',api.MyCompanyReviewsAPIView)
router.register('my-reviews',api.MyReviewsAPIView)

urlpatterns = [
    path('', include(router.urls)),
]
