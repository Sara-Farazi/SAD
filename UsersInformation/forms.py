from HotelsInformation.models import MyUser, Hotel, HotelRoom

__author__ = 'Sara-PC'
from django import forms
from HotelsInformation.models import MyUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class UserSignUpForm(forms.ModelForm):
     password = forms.CharField(label="password", widget=forms.PasswordInput)
     verified_pass = forms.CharField(widget=forms.PasswordInput ,required=True)

     class Meta:
        model = MyUser
        fields =['username','password', 'verified_pass', 'first_name', 'last_name', 'phone', 'email']
        exclude = ['password',]

     def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)

#class OwnerSignUpForm(forms.Form):


class HotelSignUpForm(forms.Form):

    #password = forms.CharField(widget=forms.PasswordInput, required=True)
   # verified_pass = forms.CharField(widget=forms.PasswordInput)
    hotel_name = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=50, required=True)
    hotel_phone = forms.CharField(max_length=30, required=True)
    hotel_email = forms.CharField(max_length=30, required=True)
    rate = forms.IntegerField(required=True)
    capacity = forms.IntegerField(required=True)


class HotelEdit(forms.ModelForm):

    hotel_name = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=50, required=True)
    hotel_phone = forms.CharField(max_length=30, required=True)
    hotel_email = forms.CharField(max_length=30, required=True)
    number_of_single_rooms = forms.IntegerField(required=True)
    number_of_double_rooms=forms.IntegerField(required=True)
    single_cost= forms.FloatField(required=True)
    double_cost= forms.FloatField(required=True)
    class Meta:
        model = Hotel
        fields =['hotel_name', 'address', 'hotel_phone', 'hotel_email']


class ActivationForm(forms.Form):
    activation_key = forms.CharField(max_length=200, required=True)


class Information(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    user_name = forms.CharField()
    email = forms.CharField()
    phone = forms.IntegerField()


class Search(forms.Form):
    ostan = forms.CharField(required=False)
    check_in = forms.DateField(required=False)
    check_out = forms.DateField(required=False)
    number_people = forms.IntegerField(required=False)
    number_room = forms.IntegerField(required=False)
    conference_room = forms.BooleanField(required=False)
    gym = forms.BooleanField(required=False)
    lunch = forms.BooleanField(required=False)
    breakfast = forms.BooleanField(required=False)
    swimming_pool = forms.BooleanField(required=False)
    internet = forms.BooleanField(required=False)
    rate = forms.IntegerField(required=False)


class reserveForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    roomType = forms.BooleanField(required=False)
    numberOfRooms = forms.IntegerField(required=True)