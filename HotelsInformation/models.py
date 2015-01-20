from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, UserManager

# Create your models here.
TYPE = (
    (1, 'single'),
    (2, 'double'),
)


class MyUser(AbstractUser):
    phone = models.CharField(max_length=11)
    is_admin = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, blank=True)


    objects = UserManager()


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    hotel_phone = models.CharField(max_length=30)
    hotel_email = models.CharField(max_length=30)
    hotel_owner = models.ForeignKey(MyUser)
    hotel_rate=models.IntegerField(max_length=1,null=True)


class HotelRoom(models.Model):
    roomNumber = models.IntegerField(null=False)
    hotel = models.ForeignKey(Hotel)
    cost = models.FloatField()
    type = models.CharField(choices=TYPE, max_length=2)








