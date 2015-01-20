from HotelsInformation.models import MyUser, Hotel

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


class HotelSignUpForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput, required=True)
    verified_pass = forms.CharField(widget=forms.PasswordInput)

    hotel_name = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=50, required=True)
    hotel_phone = forms.CharField(max_length=30, required=True)
    hotel_email = forms.CharField(max_length=30, required=True)
    number_of_single_rooms = forms.IntegerField(required=True)
    number_of_double_rooms=forms.IntegerField(required=True)
    single_cost= forms.FloatField(required=True)
    double_cost= forms.FloatField(required=True)
    class Meta:
        model = MyUser
        fields =['username', 'password', 'verified_pass', 'first_name', 'last_name', 'phone', 'email']

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

