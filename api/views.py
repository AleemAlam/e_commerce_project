from django.shortcuts import render
from .serializers import  UserProfileSerializer, ItemSerializer
from rest_framework.views import APIView
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth.models import User
from product.models import UserProfile, Item


class ProfileCreateView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(user = user)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('User is already exist')
        serializer.save(user = self.request.user)
    

class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(user = user)


class Profile(APIView):
    def get(self, request, format=None):
        try:
            user = UserProfile.objects.get(user = request.user)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except:
            raise ValidationError('You need to log in first')


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



