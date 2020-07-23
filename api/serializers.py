from rest_framework import serializers
from product.models import UserProfile, Item, Order, Cart
from django.contrib.auth.models import User


class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = UserProfile
        fields = ['id',
                  'user',
                  'country',
                  'city',
                  'phone',
                  'image']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id',
                  'title',
                  'category',
                  'description',
                  'image',
                  'discount_price',
                  'avg_rating',
                  'no_of_ratings',
                  'price']



class OrderItemSerializer(serializers.ModelSerializer):
    item = StringSerializer()
    item_obj = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'id',
            'item',
            'item_obj',
            'final_price',
            'quantity',
        )

    def get_item_obj(self, obj):
        return ItemSerializer(obj.item).data

    def get_final_price(self, obj):
        return obj.get_final_price()


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_items',
            'total',
        )

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.items.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()