from django.contrib import admin
from HotelsInformation.models import MyUser, Hotel, HotelRoom
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Hotel)
admin.site.register(HotelRoom)
