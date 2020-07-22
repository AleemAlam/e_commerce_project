from django.forms import ModelForm
from .models import Item, Category

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('title', 'price', 'category', 'description', 'image', 'discount_price')

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('title',)
