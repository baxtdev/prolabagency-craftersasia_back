from rest_framework import serializers

from rest_registration.api.serializers import DefaultUserProfileSerializer

from apps.companies.models import Company,CompanyApplication,CompanyBalance
from api.users.serializers import UserProfileSerializer

class MyCompanyBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBalance
        fields = ('id','amount','balance','days_transaction_closing','sold_items','created_at')


class MyCompanySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(source='owner',read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    balance = MyCompanyBalanceSerializer(read_only=True)
    class Meta:
        model = Company
        fields = (
            'id',
            'created_at',
            'legal_name',
            'legal_address',
            'phone',
            'city',
            'index',
            'site_url',
            'image',
            'owner',
            'user',
            'balance',
        )


    def update(self, instance, validated_data):
        image = validated_data.get('image', instance.image)
        instance.legal_name = validated_data.get('legal_name', instance.legal_name)
        instance.legal_address = validated_data.get('legal_address', instance.legal_address)
        instance.city = validated_data.get('city', instance.city)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.index = validated_data.get('index', instance.index)
        instance.site_url = validated_data.get('site_url', instance.site_url)

        if image is None and validated_data['image'] is None or not 'image' in validated_data:
            instance.save()
        
        else:
           instance.image=image 
           instance.save()

        return instance    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

class CompanySerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(read_only=True)
    class Meta:
        model = Company
        fields = '__all__'



class CompanyApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = CompanyApplication
        fields = (
            'id',
            'user',
            'legal_name',
            'legal_address',
            'phone',
            'city',
            'index',
            'site_url',
            'image'
        )



class AboutCompanySerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(read_only=True)
    class Meta:
        model = Company
        fields = (
            'id',
            'owner',
            'legal_name',
            'legal_address',
            'phone',
            'city',
            'index',
            'site_url',
            'image',
            'buys_count',
            'raiting',
            'count_of_fives',
            'count_of_fourths',
            'count_of_threes',
            'count_of_twos',
            'count_of_ones',
            'buys_count'
            )

    def to_representation(self, instance:Company):
        representation = super().to_representation(instance)

        representation['marks'] = [
            {'delivery':
             [
                {"in_last_month":instance.marks_in_last_month['delivery']},
                {"in_last_two_months":instance.marks_in_two_month['delivery']},
                {'in_last_year':instance.marks_in_last_year['delivery']}
             ]
             }, 
            {'price_relevancy':[
                {"in_last_month":instance.marks_in_last_month['price']},
                {"in_last_two_months":instance.marks_in_two_month['price']},
                {'in_last_year':instance.marks_in_last_year['price']}
             ]
             },
            {"quality":[
                {"in_last_month":instance.marks_in_last_month['quality']},
                {"in_last_two_months":instance.marks_in_two_month['quality']},
                {'in_last_year':instance.marks_in_last_year['quality']}
             ]
             }
            ]
        

        return representation