from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
import os

def getfilename(instance,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H")
    new_filename=f"{now_time}{filename}"
    return os.path.join('upload/',new_filename)


class Category(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(null=True,blank=True,upload_to=getfilename)
    description=models.CharField(max_length=150,null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0-show,1-Hide')
    created_at=models.CharField(max_length=150,null=False,blank=False)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(null=True,blank=True,upload_to=getfilename)
    image_1=models.ImageField(null=True,blank=True,upload_to=getfilename)
    image_2=models.ImageField(null=True,blank=True,upload_to=getfilename)
    image_3=models.ImageField(null=True,blank=True,upload_to=getfilename)
    description=models.CharField(max_length=150,null=False,blank=False)
    vendor=models.CharField(max_length=150,null=False,blank=False)
    orginal_price=models.IntegerField(null=False,blank=False)
    quantity=models.IntegerField(null=False,blank=False)
    selling_price=models.IntegerField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0-show,1-Hide')
    trending=models.BooleanField(default=False,help_text='0-default,1-trending')
    created_at=models.CharField(max_length=150,null=False,blank=False)

    def __str__(self):
        return self.name
    
class Cart_Page(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pro=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart_quantity=models.IntegerField(default=1)
 

    def __str__(self):
        return self.user.username
    
class favourate(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pro_duct=models.ForeignKey(Product,on_delete=models.CASCADE)
    like=models.BooleanField(default=True)

    def __str__(self):
        return self.pro_duct.name


# from django.db import models

class shipping(models.Model):

    # 🧾 Customer Info
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    # 📍 Shipping Address
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    landmark = models.CharField(max_length=100, blank=True, null=True)

    # 💳 Payment (Default = Cash on Delivery)
    # 🕒 Order Info
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
class delivery(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart_Page,on_delete=models.SET_NULL,blank=True, null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True, null=True)
    shipping_address=models.ForeignKey(shipping,on_delete=models.CASCADE,blank=True, null=True)
    amount=models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    COLOR_CHOICES = [
        (1, "Placed (Red)"),
        (2, "Shipped (Yellow)"),
        (3, "Delivered (Green)"),
        (4, "Cancelled"),
    ]
    color = models.IntegerField(choices=COLOR_CHOICES, default=1)
    def __str__(self):
        if self.cart and self.cart.pro:
            return f"{self.cart.pro.name} for {self.user.username}"
        else:
            return f"Delivery for {self.user.username} (no product)"

class FeedBack(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    testimonial=models.CharField(null=False,blank=False,max_length=238)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    query_type = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username