from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('J', 'Jeans'),
    ('SW', 'Sport Wear'),
    ('OW', 'Outwear'),
)

class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    description = models.TextField()
    image = models.ImageField('items')
    discount_price = models.FloatField(blank=True, null=True)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(item=self)
        return len(ratings)
    
    def avg_rating(self):
        ratings = Rating.objects.filter(item=self)
        sum=0
        for rating in ratings:
            sum += rating.rating
        if len(ratings)>0:
            return sum/len(ratings)
        else:
            return None
    

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    item = models.ForeignKey(Item, related_name='cart_item', on_delete= models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def __str__(self):
        return self.item.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    items = models.ManyToManyField(Cart)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=400)
    billing_address = models.CharField(max_length=400)
    received = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def __str__(self):
        return self.user.username

class Rating(models.Model):
    item = models.ForeignKey(Item, related_name='item', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    class Meta:
        unique_together = (('user', 'item'),)
        index_together = (('user', 'item'),)

    def __str__(self):
        return self.item.title
