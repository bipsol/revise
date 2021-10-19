from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    image  = models.ImageField(upload_to='category/', default='img.jpeg')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category =models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)    
    price = models.FloatField()  #it's better to use integerfield or floatfield
    min_quantity = models.IntegerField(default=1)  
    max_quantity = models.IntegerField(default=20)  
    image  = models.ImageField(upload_to='shop/', default='img.jpeg')
    description = models.TextField()
    available = models.BooleanField()
    featured = models.BooleanField(default=False)
    new_arrival = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile/', default='profile.jpeg', blank=True, null=True)


    def __str__ (self):
        return self.first_name

    class Meta:
        db_table = 'profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart_code = models.CharField(max_length=50)
    paid_order = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username 



class PaidOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_paid = models.IntegerField()
    cart_code = models.CharField(max_length=36)
    transac_code = models.CharField(max_length=10)
    paid_order = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username 

    





