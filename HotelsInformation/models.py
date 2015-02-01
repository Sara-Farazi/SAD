# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, UserManager

# Create your models here.

COMMENT_STATUS = (
    (0, ('Pending')),
    (1, ('Accept')),
    (2, ('Reject')),
)

province = (
    (0, ('آذربایجان غربی')),
    (1, ('اردبیل')),
    (2, ('اصفهان')),
    (3, ('البرز')),
    (4, ('ایلام')),
    (5, ('بوشهر')),
    (6, ('تهران')),
    (7, ('چهار محال و بختیاری')),
    (8, ('خراسان جنوبی')),
    (9, ('خراسان رضوی')),
    (10, ('خراسان شمالی')),
    (11, ('خوزستان')),
    (12, ('زنجان')),
    (13, ('سمنان')),
    (14, ('سیستان و بلوچستان')),
    (15, ('فارس')),
    (16, ('قزوین')),
    (17, ('قم')),
    (18, ('کردستان')),
    (19, ('کرمان')),
    (20, ('کرمانشاه')),
    (21, ('کهگیلویه و بویراحمد')),
    (22, ('گلستان')),
    (23, ('گیلان')),
    (24, ('لرستان')),
    (25, ('مازندران')),
    (26, ('مرکزی')),
    (27, ('هرمزگان')),
    (28, ('همدان')),
    (29, ('یزد')),
    (30,('آذربایجان شرقی'))

)


class MyUser(AbstractUser):
    phone = models.CharField(max_length=11)
    is_admin = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, blank=True)


    objects = UserManager()




class Hotel(models.Model):
    ostan = models.IntegerField(choices=province, max_length=100, default=0)
    hotel_name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    hotel_phone = models.CharField(max_length=30)
    hotel_email = models.CharField(max_length=30)
    hotel_owner = models.ForeignKey(MyUser)
    hotel_rate=models.IntegerField(max_length=1)
    given_rate = models.IntegerField(max_length=1,null= True)
    conference_room = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    #numberOfrooms = models.IntegerField()
    capacity = models.IntegerField(max_length=4)
    is_accepted = models.BooleanField(default=False)



class RoomType(models.Model):
    numberOfType = models.IntegerField()


class HotelRoom(models.Model):
    roomNumber = models.IntegerField(null=True)
    hotel = models.ForeignKey(Hotel)
    cost = models.FloatField()
    metraj = models.FloatField()
    view = models.CharField(max_length=20)
    is_reserved = models.BooleanField(default=False)
    capacity = models.IntegerField(max_length=100)
    type = models.CharField(max_length=100,null = False)
    numberOfType = models.IntegerField()



class Picture(models.ImageField):
    pic= models.ImageField(null=False)
    hotel = models.ForeignKey(HotelRoom , null= True)
    room= models.ForeignKey(Hotel, null=True)



class Reserve(models.Model):
    checkin =models.DateTimeField(null = True)
    checkout = models.DateTimeField(null = True)
    user = models.ForeignKey(MyUser , null=False)
    hotel = models.ForeignKey(Hotel , null=False)
    payment = models.FloatField(max_length=100 , null=False)
    number_people = models.IntegerField(max_length=100, null=True)
    number= models.IntegerField(null=True)
    type=models.CharField(max_length=100,null=False)




class Comment(models.Model):
    name = models.CharField(u'نام', max_length=200)
    email = models.EmailField(u'ایمیل')
    date = models.DateTimeField(u'تاریخ :', auto_now=True)
    body = models.TextField(u'')
    hotel = models.ForeignKey(Hotel)
    user = models.ForeignKey(MyUser, related_name="comments", null=True, blank=True)
    status = models.IntegerField(choices=COMMENT_STATUS, max_length=10, default=0)

    def __str__(self):
        return self.name

