from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,default='')
    image = models.ImageField(upload_to='profile_image', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.title

STATUS = (
    ('OK', 'OK'),
    ('NOT_OK', 'NOT_OK')
)

class Item(models.Model):

    title = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(choices= STATUS ,max_length=10, default='OK')
    image = models.ImageField('items')
    discount_price = models.FloatField(blank=True, null=True, default=0)

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
    item = models.ForeignKey(Item, related_name='item', on_delete= models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
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

    @property
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


    def __str__(self):
        for item in self.items.item:
            print('this is item',item)

        return self.user.username

class Rating(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    class Meta:
        unique_together = (('user', 'item'),)
        index_together = (('user', 'item'),)

    def __str__(self):
        return self.item.title

class ShippingAddress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete= models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.address+ ' address of ' + self.user.user.username


PAYMENT_STATUS=(
    ('APPROVED', 'APPROVED'),
    ('PENDING', 'FALIURE'),
)

class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    razorpay_payment_id = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices= PAYMENT_STATUS, max_length=50)
    amount = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

