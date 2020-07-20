from django.contrib import admin
from .models import Item, Cart, Order, Rating
# Register your models here.

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Rating)