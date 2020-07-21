from django.forms import ModelForm
from .models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('title', 'price', 'category', 'description', 'image', 'discount_price')
