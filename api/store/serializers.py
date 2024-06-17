from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

from api.companies.serializers import CompanySerializer

from api.users.serializers import UserProfileSerializer
from apps.store.models import (
    ItemModel,
    ItemImages,
    Item,
    ItemCategory,
    ItemSubCategory,
    Color,Currency,
    ItemPayment,
    FavoriteItems,
    ItemReviews,
    ItemModelName
    )
from apps.users.models import User

#colors
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

#currency
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

#ctagories
class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = '__all__'

#subcategories
class ItemSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSubCategory
        fields = '__all__'

#images
class ItemModelImageSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ItemImages
        fields = ('id','image')

#Item models Create For Companies
class ItemModelCretaeSerializer(serializers.ModelSerializer):
    images = ItemModelImageSerailizer(
        many = True,
        read_only = True
    )
    set_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000,allow_empty_file=False,use_url=True),
        write_only=True,
        required=False
        )
    rm_items_list = serializers.PrimaryKeyRelatedField(
        queryset=ItemImages.objects.all(),
        write_only=True,
        required=False,
        many=True
    )

    
    class Meta:
        model = ItemModel
        fields = ('id','item','name_model','color','quantity','price','discount','currency','images','set_images','rm_items_list')
    
    @transaction.atomic  
    def create(self, validated_data):
        images_data = validated_data.pop('set_images',None)
        name = validated_data.get('name_model',None)
        
        validated_data.pop('rm_items_list')
        
        item_model = ItemModel.objects.create(**validated_data)

        item_model_name,created = ItemModelName.objects.get_or_create(name=name,item=item_model.item)

        item_model.item_model =item_model_name
        item_model.save()

        if images_data:
            for image in images_data:
                ItemImages.objects.create(item_model=item_model,image=image)

        return item_model
    
    @transaction.atomic
    def update(self, instance, validated_data):
        instance.item = validated_data.get('item', instance.item)
        instance.name_model = validated_data.get('name_model', instance.name_model)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.price = validated_data.get('price', instance.price)
        instance.currency = validated_data.get('currency', instance.currency)

        colors = validated_data.pop('set_color', None)
        colors_data = colors.replace('[','').replace(']','').replace('*','').strip() if colors else None
        if colors_data:
            instance.color.clear()
            for color_id in colors_data:
                try:
                    color_id = int(color_id)
                    color = Color.objects.get(id=color_id)
                    instance.color.add(color)
                except:
                    continue

        rm_items_data = validated_data.get('rm_items_list', None)
        if rm_items_data:
            for item in rm_items_data:
                if item.item_model.item==instance.item_model.item:
                    item.delete()           
                    # try:
                    #     ItemImages.objects.get(id=item.id).delete()

                    # except ItemImages.DoesNotExist:
                    #     continue
        
        images_data = validated_data.get('set_images')
        if images_data:
            for image in images_data:
                ItemImages.objects.get_or_create(item_model=instance, image=image)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance) 
        representation['color'] = ColorSerializer(instance.color).data
        representation['currency'] = CurrencySerializer(instance.currency).data
        return representation


#Item Create for Companies
class ItemCreateSerializer(serializers.ModelSerializer):
    company_owner = CompanySerializer(source='company',read_only=True)
    class Meta:
        model = Item
        fields = ('id','name','category','subcategory','description','main_features','price','discount_price','code','is_new','is_popular','raiting','company_owner')

        read_only_fields = ('code','is_new','is_popular','company_owner')


    def create(self, validated_data):
        user:User = self.context['request'].user

        validated_data['company'] = user.company

        item = Item.objects.create(**validated_data)
        return item    


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_url = None
        first_model = instance.models.first()
        if first_model:
            first_image = first_model.images.first()
            if first_image:
                image_url = self.context['request'].build_absolute_uri(first_image.image.url)
        representation['image'] = image_url
        if instance.models.first():
            representation['currency'] = CurrencySerializer(instance.models.first().currency).data

        representation['category'] = ItemCategorySerializer(instance.category).data
        representation['subcategory'] = ItemSubcategorySerializer(instance.subcategory).data
            
        return representation

#Item Payments
class ItemPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPayment
        fields = '__all__'


#item Models List 
class ItemModelSerializer(serializers.ModelSerializer):
    images = ItemModelImageSerailizer(
        many=True,
    )
    
    class Meta:
        model = ItemModel
        fields = ('id','color','quantity','price','discount','currency','images')
    def to_representation(self, instance):
        representation = super().to_representation(instance) 
        representation['color'] = ColorSerializer(instance.color).data
        representation['currency'] = CurrencySerializer(instance.currency).data
        return representation 


#Item Model Names
class ItemModelnameSerializer(serializers.ModelSerializer):
    colors = ItemModelSerializer(many=True,read_only=True)
    class Meta:
        model = ItemModelName
        fields = ('name','colors')

       
#Item Detail List For all
class ItemDetailSerializer(serializers.ModelSerializer):
    models_name = ItemModelnameSerializer(many=True,read_only=True)
    payment = ItemPaymentSerializer(source="payments",read_only=True)
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'category',
            'subcategory',
            'description',
            'main_features',
            'company',
            'payment',
            'code',
            'is_new',
            'is_popular',
            'raiting',
            'models_name',
            'views_count',
            'raiting',
            'buys_count',
            'favorites_count',
        )
        

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = ItemCategorySerializer(instance.category).data
        representation['subcategory'] = ItemSubcategorySerializer(instance.subcategory).data
        return representation


#Item Details For Companies and Create
class MyItemDetailSerializer(serializers.ModelSerializer):
    models = ItemModelCretaeSerializer(
        many = True,
        read_only = True
    )
    payment = ItemPaymentSerializer(source="payments",read_only=True)
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'category',
            'subcategory',
            'description',
            'main_features',
            'models',
            'company',
            'payment',
            'code',
            'description',
            'is_new',
            'is_popular',
            'views_count',
            'raiting',
            'buys_count',
            'favorites_count',
            )
                
        read_only_fields = ('is_new','is_popular','views_count')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = ItemCategorySerializer(instance.category).data
        representation['subcategory'] = ItemSubcategorySerializer(instance.subcategory).data
        return representation


#Favorit Tours
class FavoriteItemsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    item_data = ItemCreateSerializer(
        source="item",
        read_only=True
        )

    class Meta:
        model = FavoriteItems
        fields = '__all__'

        extra_kwargs = {
            'item': {'write_only': True},
        }    
   

#Item Reviews for all
class ItemReviewsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model = ItemReviews
        fields = (
            'id',
            'order',
            'company',
            'company',
            'item',
            'user',
            'delivery',
            'quality',
            'price_relevance',
            'advantages',
            'disadvantages',
            'comment'
            )      


#item review lists
class ItemReviewsListSerializer(serializers.ModelSerializer ):
    user = UserProfileSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    item = ItemCreateSerializer(read_only=True)
    class Meta:
        model = ItemReviews
        fields = (
            'id',
            'order',
            'company',
            'item',
            'user',
            'delivery',
            'quality',
            'price_relevance',
            'advantages',
            'disadvantages',
            'comment'
            )

        