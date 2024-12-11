
from django.db import models
from django.contrib.auth.models import User
from django.db import models
import datetime
import os


def img_file_name(request,filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class Catagory(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=img_file_name, null=True, blank=True)
    banner_image = models.ImageField(upload_to=img_file_name, null=True, blank=True)
    description = models.TextField(max_length=700, null=False, blank=False)
    status = models.BooleanField(default=False, help_text=("0-show,1-Hidden"))
    created_at = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(upload_to=img_file_name, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Products(models.Model):

    catagory = models.ForeignKey(Catagory,on_delete=models.CASCADE)

    name = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=img_file_name, null=True, blank=True)
    manufacture = models.CharField(max_length=300, null=False, blank=False)
    vendor = models.CharField(max_length=300, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    incredients = models.TextField(max_length=3000, null=True, blank=False)
    benefits= models.TextField(max_length=3000, null=True, blank=False)
    doses = models.TextField(max_length=1000, null=True, blank=False)
    status = models.BooleanField(default=False, help_text=("0-show,1-Hidden"))
    trending = models.BooleanField(default=False, help_text=("0-default,1-Trending"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    # models.py

    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_Cost(self):
        return self.product_qty * self.product.price
    

class CarouselItem(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='carousel_images/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Favourite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CategoryBanner(models.Model):
    category = models.ForeignKey(Catagory,on_delete=models.CASCADE)
    banner_image = models.ImageField(upload_to='banners/', null=True, blank=True)
    alt_text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.category.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    


class Product(models.Model):

    name = models.CharField(max_length=255)
    price = models.FloatField(null=False, blank=False)
    
    def __str__(self):
        return self.name
    



class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    notes = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # 'items' is the custom related name
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Poster(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.title


