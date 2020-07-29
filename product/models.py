from django.db import models
import binascii
import os
from django.contrib.auth.models import User


def beer_directory_path(instance, filename):
    return os.path.join(str(instance.name), "{}.{}".format(filename.split('.')[0], filename.split('.')[-1]))

class Category(models.Model):
    name =  models.CharField(max_length=256)
    class Meta:
        db_table = 'product_category'

class Product(models.Model):
    name = models.CharField(max_length=256)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=beer_directory_path, null=True)
    price = models.FloatField()
    class Meta:
        db_table = 'product_product'

class Order(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    money = models.FloatField()
    number = models.IntegerField()
    iteam_code = models.IntegerField()
    class Meta:
        db_table = 'product_order'

    