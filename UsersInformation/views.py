import email
import hashlib
import random
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from setuptools.compat import unicode
from HotelsInformation.models import MyUser, Hotel, HotelRoom
from UsersInformation.forms import LoginForm, UserSignUpForm, HotelSignUpForm, HotelEdit, ActivationForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
__author__ = 'Sara-PC'


def hotel_viewer(request):
        pass

def signin(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = LoginForm(request.POST)  # A form bound to the POST data
        print(form)
        if form.is_valid():  # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']


            user = authenticate(username=username, password=password)

            if (user is not None) and user.is_active:
                print("login page none nist")
                login(request, user)
                print("login shodam")
                return HttpResponseRedirect("/userprofile/")
            else:
                form.errors[''] = 'wrong username or password'
    else:
        form = LoginForm()  # An unbound form
   # hotels = Hotel.objects.all()

<<<<<<< HEAD
    return render(request, 'login.html', {'form': form})
=======
    return render(request, 'home.html', {'form': form})
>>>>>>> 67a998d2dca3776887942939b3efb7b28ffb47ec
    #return render(request, 'loginPae.html', {'form': form, 'hotels':hotels, 'user':user})

def signout(request):
	return logout(request)



def Userregister(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            #form.save()
            email = form.cleaned_data['email']
            user = MyUser.objects.create_user(form.cleaned_data['username'],email, form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone = form.cleaned_data['phone']
            rand=str(random.random()).encode('utf-8')
            salt = hashlib.sha1(rand).hexdigest()[:5]
            salt_bytes = salt.encode('utf-8')
            if isinstance(email, unicode):
                emaile = email.encode('utf-8')
            activation_key = hashlib.sha1(salt_bytes+emaile).hexdigest()


            user.activation_key = activation_key
            user.is_active = False
            user.save()
            send_mail('Account Confirmation', activation_key , 'simorgh9394@gmail.com', [email])
            print("bade send mail")
            return HttpResponseRedirect("/activation/")

    else:
        form = UserSignUpForm()


    return render(request, 'usersignup.html', {'form': form})


def Hotelregister(request):
    if request.method == 'POST':
        form = HotelSignUpForm(request.POST)
        if form.is_valid():
            print("HEY")
            email = form.cleaned_data['email']
            user = MyUser.objects.create_user(form.cleaned_data['username'],email, form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.is_active = False
            user.is_owner = True

            rand=str(random.random()).encode('utf-8')
            salt = hashlib.sha1(rand).hexdigest()[:5]
            salt_bytes = salt.encode('utf-8')
            if isinstance(email, unicode):
                emaile = email.encode('utf-8')
            activation_key = hashlib.sha1(salt_bytes+emaile).hexdigest()
            user.activation_key = activation_key
            user.save()
            hotel = Hotel()
            hotel.address = form.cleaned_data['address']
            hotel.hotel_email = form.cleaned_data['hotel_email']
            hotel.hotel_name = form.cleaned_data['hotel_name']
            hotel.hotel_phone = form.cleaned_data['hotel_phone']
            hotel.hotel_owner = user
            hotel.save()


            single_room = form.cleaned_data['number_of_single_rooms']
            double_room = form.cleaned_data['number_of_double_rooms']
            print("ghable for")
            for i in range(0,single_room):

                hotelroom1=HotelRoom()
                cost=form.cleaned_data['single_cost']
                hotelroom1.cost=cost
                hotelroom1.roomNumber=hotel.id + i
                hotelroom1.hotel=hotel
                hotelroom1.type=1
                hotelroom1.save()
                print("bade save hotelroom")




            for i in range(0,double_room):
                hotelroom2=HotelRoom()
                cost=form.cleaned_data['double_cost']
                hotelroom2.cost=cost
                hotelroom2.roomNumber=hotel.id+i
                hotelroom2.hotel=hotel
                hotelroom2.type=2
                hotelroom2.save()
            send_mail('Account Confirmation', activation_key , 'simorgh9394@gmail.com', [email])
            return HttpResponseRedirect("/activation/")
    else:
        form = HotelSignUpForm()

    return render(request, 'hotelsignup.html', {'form': form})


def UserEdit(request):
    user = MyUser.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        print("post")
        form = UserSignUpForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/userprofile/")
        else:
            print(form)

    else:
        form = UserSignUpForm(instance=user)

    name=user.first_name
    family=user.last_name
    username= user.username
    phone=user.phone
    email=user.email

    return render(request, 'useredit.html', {'form': form, 'name':name,'family':family,'username':username,'phone':phone,'email':email})


@login_required(redirect_field_name='my_redirect_field')
def hotelEdit(request,hotel_id):
    hotel = Hotel.objects.get(id=int(hotel_id))
    user = MyUser.objects.get(pk=request.user.pk)
    hotelroom1=HotelRoom.objects.get(hotel=hotel,type=1,roomNumber=hotel.id+1)
    hotelroom2=HotelRoom.objects.get(hotel=hotel,type=2,roomNumber=hotel.id+1)

    if request.method == 'POST':
        print("post")
        form = HotelEdit(request.POST,instance=hotel)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/userprofile/")
        else:
            print(form)

    else:
        form = HotelEdit(instance=hotel)

    name=hotel.hotel_name
    address=hotel.address
    email= hotel.hotel_email
    phone=hotel.hotel_phone
    owner=hotel.hotel_owner
    single_cost=hotelroom1.cost
    double_cost=hotelroom2.cost

    if user.is_owner == True and user.id == hotel.hotel_owner.id:
        return render(request, 'hoteledit.html', {'form': form, 'name':name,'address':address,'email':email,'phone':phone,'owner':owner,'single_cost':single_cost,'double_cost':double_cost})

    else:
        return render(request, 'error.html', {'form': form, 'username': user.username, 'password':user.password})
#not for this phase
def my_hotel(request):
    user = MyUser.objects.get(id=request.user.id)
    hotels = Hotel.objects.filter(hotel_owner=user)
    return render(request, 'hedit.html', {'hotels': hotels})

def HotelProfile(request):
    user = MyUser.objects.get(pk=request.user.pk)
    hotels = Hotel.objects.filter(hotel_owner=user)
    id = request.user.id
    return render(request, 'hotelprofile.html', {'user': user,'hotels':hotels, 'id':id})


def UserProfile(request):
    user = MyUser.objects.get(pk=request.user.pk)
    hotels = Hotel.objects.filter(hotel_owner=user)
    return render(request, 'userprofile.html', {'user': user,'hotels':hotels})

def activation(request):
    if request.method == 'POST':
        print("post")
        form = ActivationForm(request.POST)
        if form.is_valid():
            user = MyUser.objects.get(activation_key=form.cleaned_data['activation_key'])
            #user = authenticate(activation_key=form.cleaned_data['activation_key'])
            print("user pas none")
            #user = authenticate(activation_key=form.cleaned_data['activation_key'])


                #login(request, user)
            user.is_active=True
            user.save()

            return HttpResponseRedirect("/login/")

    else:
        form = ActivationForm()

    #code = user.activation_key
    return render(request, 'activation.html', {'form':form})