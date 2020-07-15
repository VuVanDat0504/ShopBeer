from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
USER_TYPE_CHOICES = (
    (1, 'admin'),
    (2, 'user'),
)
GENDER_CHOICES = (
    (1, 'admin'),
    (2, 'user'),
)

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender =  models.PositiveSmallIntegerField(choices=GENDER_CHOICES)
    age = models.IntegerField()
    class Meta:
        db_table = 'users_user'
