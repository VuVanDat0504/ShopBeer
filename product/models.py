from django.db import models
import binascii
import os
from django.contrib.auth.models import User


def beer_directory_path(instance, filename):
    return os.path.join(str(instance.name), "{}.{}".format(filename.split('.')[0], filename.split('.')[-1]))

class Beer(models.Model):
    name = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    picture = models.ImageField(upload_to=beer_directory_path, null=True)
    class Meta:
        db_table = 'product_beer'

class Order(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    product =  models.ForeignKey(Beer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    money = models.FloatField()
    number = models.IntegerField()
    class Meta:
        db_table = 'product_order'

    