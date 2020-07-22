from django.contrib import admin
from .models import Item, Cart, Order, Rating, Category, UserProfile
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Rating)