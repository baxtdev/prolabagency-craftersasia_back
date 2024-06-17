import django_filters

from apps.order.models import Order,OrderItems

class OrderFilter(django_filters.FilterSet):
    user__email = django_filters.CharFilter(field_name='user__email', lookup_expr='icontains', label='Email пользователя')
    items__item__name = django_filters.CharFilter(field_name='items__item__name', lookup_expr='icontains', label='Название товара')
    items__company__legal_name = django_filters.CharFilter(field_name='items__company__legal_name', lookup_expr='icontains', label='Название компании')


    class Meta:
        model = Order
        fields = ('user__email', 'items__item__name','items__company__legal_name')


class OrderItemFilter(django_filters.FilterSet):
    item__name = django_filters.CharFilter(field_name='item__name', lookup_expr='icontains', label='Название товара')
    item__description = django_filters.CharFilter(field_name='item__description', lookup_expr='icontains', label='Описание товара')
    item_model__item_model__name = django_filters.CharFilter(field_name='item_model__item_model__name', lookup_expr='icontains', label='Название модели товара')
    color__name = django_filters.CharFilter(field_name='color__name', lookup_expr='icontains', label='Название цвета')

    class Meta:
        model = OrderItems
        fields = (
            'item__name',
            'item__description',
            'item_model__item_model__name',
            'color__name'
            )        