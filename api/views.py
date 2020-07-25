from django.shortcuts import render, get_object_or_404
from .serializers import  UserProfileSerializer, ItemSerializer, OrderSerializer
from rest_framework.views import APIView
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from product.models import UserProfile, Item, Cart, Order
from django.core.exceptions import ObjectDoesNotExist


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(user = user)


class Profile(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        try:
            _profile = request.user.userprofile
        except ObjectDoesNotExist:
            _profile = {
                "phone": '',
                "image": '',
            }
        finally:
            content = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                'phone': _profile.phone,
                'image': _profile.image
            }
            return Response(content, status=200)


class ProductList(APIView):
    def get(self, request, format=None):
        item = Item.objects.filter(status = 'OK')
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.is_authenticated:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise ValidationError('You need to Login First')

class Product(APIView):
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise ValidationError('Product id is invalid')

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if request.user.is_authenticated:
            item = self.get_object(pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise ValidationError('You need to Login First')


    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.status = 'NOT_OK'
        item.save()
        return Response({'message': 'content is deleted'}, status=status.HTTP_204_NO_CONTENT)


class AddToCart(APIView):
    def post(self, request, pk, *agrs, **kwargs):
        if pk is None:
            return Response({'message':'invalid response'}, status = status.HTTP_400_BAD_REQUEST)
        item = get_object_or_404(Item, pk=pk)
        order_item, created = Cart.objects.get_or_create(
            item = item,
            user = request.user,
            ordered = False,
        )
        order_qs = Order.objects.filter(user = request.user, ordered = False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__id = item.id).exists():
                order_item.quantity +=1
                order_item.save()
                return Response({'message':'Product Added Successfully'},status= status.HTTP_200_OK)
            else:
                order.items.add(order_item)
                return Response({'message':'Product Added Successfully'},status= status.HTTP_200_OK)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user = request.user, ordered_date = ordered_date,
            )
            order.items.add(order_item)
            return Response({'message':'Product Added Successfully'},status= status.HTTP_200_OK)





class OrderDetailsView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self):
        try:
            order = Order.objects.get(user= self.request.user, ordered = False)
            return order
        except ObjectDoesNotExist:
            return Response({"message":"You don't have any order"}, status= status.HTTP_400_BAD_REQUEST)


