from rest_framework import serializers
from product.models import UserProfile, Item
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = UserProfile
        fields = ['id','user','country', 'city', 'phone', 'image']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id','title', 'category', 'description', 'image', 'discount_price', 'avg_rating', 'no_of_ratings' ,'price']

