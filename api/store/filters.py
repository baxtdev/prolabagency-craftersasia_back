from django_filters import FilterSet,NumberFilter
import django_filters

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from apps.store.models import ItemSubCategory,Item,ItemReviews,ItemCategory,ItemSubCategory,FavoriteItems

class ItemCategoryFilter(FilterSet):
    class Meta:
        model = ItemCategory
        fields = ('name',)


class ItemSubCategoryFilter(FilterSet):
    class Meta:
        model = ItemSubCategory
        fields = ('category','name')


class ItemReviewFilter(FilterSet):
    delivery = django_filters.NumberFilter(
        field_name='delivery',
        label=_("Оценка для доставки"),
        lookup_expr='exact',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    quality = django_filters.NumberFilter(
        field_name='quality',
        label=_("Оценка для качества"),
        lookup_expr='exact',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    price_relevance = django_filters.NumberFilter(
        field_name='price_relevance',
        label=_("Оценка для актуальности цены"),
        lookup_expr='exact',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    class Meta:
        model = ItemReviews
        fields = ('item','company','order','delivery', 'quality', 'price_relevance')    


class ItemFilter(FilterSet):
    min_price = NumberFilter(field_name='models__price', lookup_expr='gte',label='Минимальная цена')
    max_price = NumberFilter(field_name='models__price', lookup_expr='lte',label='Максимальная цена')
    name = django_filters.CharFilter(label='Название')
    description = django_filters.CharFilter(label='Описание')
    models__color = django_filters.CharFilter(label='Цвет модели')
    models_name__name = django_filters.CharFilter(label='Название модели')
    
    class Meta:
        model = Item
        fields = (
            'name',
            'category',
            'subcategory',
            'description',
            'company',
            'code',
            'description',
            'is_new',
            'is_popular',
            'min_price',
            'max_price',
            'models__color',
            'models_name__name'
            )


class FavoriteItemsFilter(FilterSet):
    class Meta:
        model = FavoriteItems
        fields = ('item__name','item__description')