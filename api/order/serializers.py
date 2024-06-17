from rest_framework import serializers

from apps.order.models import Order,OrderItems

from api.store.serializers import ItemCreateSerializer,ItemModelCretaeSerializer
from api.users.serializers import UserProfileSerializer
class OrderItemSerializer(serializers.ModelSerializer):
    item_data = ItemCreateSerializer(source='item',read_only=True)
    class Meta:
        model = OrderItems
        fields = (
            'id',
            'created_at',
            'updated_at',
            'quantity',
            'item',
            'item_model',
            'item_data',
            'item_totals',
            'status',
            'company'
            )
        read_only = ('status',)

    def to_representation(self, instance):
        representetion = super().to_representation(instance)
        representetion['item_price'] = {'price':instance.item_model.price,'currency':instance.item_model.currency.code}
        return representetion



class OrderListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemListSerializer(serializers.ModelSerializer):
    item_data =  ItemCreateSerializer(source='item',read_only=True)
    item_model_data =  ItemModelCretaeSerializer(source='item_model',read_only=True)
    order = OrderListSerializer(read_only=True)
    class Meta:
        model = OrderItems
        fields = (
            'id',
            'order',
            'created_at',
            'updated_at',
            'quantity',
            'item_data',
            'item_totals',
            'status',
            'item_model_data'
        )

        read_only_fields = ('quantity','order','item_data','item_model_data')


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'created_at',
            'updated_at',
            'name',
            'phone',
            'comment',
            'status',
            'total',
            'items'
            )

        read_only_fields = ('status',)

    def create(self, validated_data):
        items = validated_data.pop('items',None)
        order = Order.objects.create(**validated_data)

        for item_data in items:
            OrderItems.objects.create(order=order,**item_data)
        return order
            




