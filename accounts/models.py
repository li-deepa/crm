from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    profile_pic= models.ImageField(default="3.JPG",null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    #name=models.CharField(max_length=200)

    def __str__(self):
        # return self.user
        return str(self.user) if self.user else ''

class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    CATEGORY=(
              ('Indoor','Indoor'),
              ('Out door','Out door'),

    )
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    description=models.CharField(max_length=200,null=True,blank=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    tags=models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.name



class Order(models.Model):
    STATUS=(
        ('pending','pending'),
        ('out for delivery','out for delivery'),
        ('delivered','delivered')
    )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    


    def __str__(self) -> str:
        return self.product.name



        