from django.urls import path, include
from . import views
from rest_framework import routers
'''
router = routers.DefaultRouter()
router.register( 'add_profile', views.UserProfileViewSet )
'''
urlpatterns = [
    path('create_profile/', views.ProfileCreateView.as_view()),
    path('', views.Profile.as_view()),
    path('<int:pk>/', views.Profile.as_view()),
    path('update_profile/<int:pk>/', views.ProfileUpdateAPIView.as_view()),
    path('all_product/', views.ProductList.as_view()),
    path('product/<int:pk>/', views.Product.as_view()),
]