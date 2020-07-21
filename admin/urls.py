from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin, name= "admin_dashboad" ),
    path('products/', views.product_list, name= "admin_products" ),
    path('add_product/', views.add_product, name= "add_product" ),
    path('admin_login/', views.admin_login, name= "admin_login" ),
    path('all_user/', views.user_list, name= "admin_alluser" ),
    path('logout/', views.admin_logout, name= "admin_logout" ),
    path('product_details/<int:pk>/', views.product_details, name= "product_details" ),
    path('delete_product/<int:pk>/', views.delete_product, name= "delete_product" ),
]
