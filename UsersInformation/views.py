import email
import hashlib
import random
import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from setuptools.compat import unicode
from HotelsInformation.models import MyUser, Hotel, HotelRoom, Reserve, Comment,RoomType
from UsersInformation.forms import LoginForm, UserSignUpForm, HotelSignUpForm, HotelEdit, ActivationForm, Search
from django.core.mail import send_mail
from UsersInformation.forms import Information
from django.contrib.auth.decorators import login_required
__author__ = 'Sara-PC'


def hotel_viewer(request):
        pass

def eror(request):
    return render(request, 'error.html')

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

    return render(request, 'login.html', {'form': form})
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


    return render(request, 'usersign.html', {'form': form})


def Hotelregister(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
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

            send_mail('Account Confirmation', activation_key , 'simorgh9394@gmail.com', [email])
            return HttpResponseRedirect("/activation/")
    else:
        form = UserSignUpForm()

    return render(request, 'hotelsign.html', {'form': form})


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


    if request.method == 'POST':
        print("post")
        form = HotelEdit(request.POST,instance=hotel)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/hotel/"+str(hotel_id))
        else:
            print(form)

    else:
        form = HotelEdit(instance=hotel)

    name=hotel.hotel_name
    address=hotel.address
    email= hotel.hotel_email
    phone=hotel.hotel_phone
    owner=hotel.hotel_owner


    #if user.is_owner == True and user.id == hotel.hotel_owner.id:
    return render(request, 'hoteledit.html', {'form': form, 'name':name,'address':address,'email':email,'phone':phone,'owner':owner})

    #else:
        #return render(request, 'error.html', {'form': form, 'username': user.username, 'password':user.password})
#not for this phase
def my_hotel(request):
    user = MyUser.objects.get(id=request.user.id)
    hotels = Hotel.objects.filter(hotel_owner=user)
    return render(request, 'hedit.html', {'hotels': hotels})

#def HotelProfile(request):
#    user = MyUser.objects.get(pk=request.user.pk)
#    hotels = Hotel.objects.filter(hotel_owner=user)
#    rooms = HotelRoom.objects.filter(hotel=hotels)
#    id = request.user.id
#    return render(request, 'hotelprofile.html', {'user': user,'hotels':hotels, 'id':id})


def UserProfile(request):
    user = MyUser.objects.get(pk=request.user.pk)
    info_form = Information(request.POST)
    hotels = Hotel.objects.filter(hotel_owner=user)
    comments = Comment.objects.filter(user=request.user)
    reserves = Reserve.objects.filter(user=request.user)
    if request.method == 'POST':
        if info_form.is_valid():
            user.first_name = info_form.cleaned_data['first_name']
            user.last_name = info_form.cleaned_data['last_name']
            user.username = info_form.cleaned_data['user_name']
            user.email = info_form.cleaned_data['email']
            user.phone = info_form.cleaned_data['phone']
            user.save()

        else:
            print("Not Valid Dude!")
            info_form = Information()

    return render(request, 'userprofile.html', {'user': user, 'hotels': hotels, 'form':info_form, 'comments':comments, 'reserves': reserves})

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

            return HttpResponseRedirect("/home/")

    else:
        form = ActivationForm()

    #code = user.activation_key
    return render(request, 'activation.html', {'form':form})



def AddHotel(request):
    if request.method == 'POST':
        form = HotelSignUpForm(request.POST)
        if form.is_valid():
            print("HEY")
            user = MyUser.objects.get(id = request.user.pk)
            hotel = Hotel()
            hotel.address = form.cleaned_data['address']
            hotel.hotel_email = form.cleaned_data['hotel_email']
            hotel.hotel_name = form.cleaned_data['hotel_name']
            hotel.hotel_phone = form.cleaned_data['hotel_phone']
            hotel.hotel_owner = user
            hotel.hotel_rate = form.cleaned_data['rate']
            hotel.capacity = form.cleaned_data['capacity']
            print(form.cleaned_data['rate'])

            hotel.save()


            print("bade save")

            return HttpResponseRedirect("/userprofile/")
    else:
        form = HotelSignUpForm()

    return render(request, 'addhotel.html', {'form': form})





#def search(request):
#    print("SEARCH")
#    if request.method =='POST':
#        form = Search(request.POST)
#        if form.is_valid():
#            all_hotels = Hotel.objects.filter(is_accepted=True)
#            for k,v in form.cleaned_data.iteritems():
#                if v and k!='None':
#                    all_hotels = all_hotels.filter(**{k: v})
#            return render(request, 'searchresults.html', {'hotels':all_hotels})
#    else:
#        form = Search()
#
#    return render(request, 'searchresults.html', {'form':form})


def search(request):
    print("SEARCH")
    if request.method =='POST':
        form = Search(request.POST)
        if form.is_valid():
            ostan = form.cleaned_data['ostan']
            begin_form = form.cleaned_data['check_in']
            end_form = form.cleaned_data['check_out']
            number_people = form.cleaned_data['number_people']
            number_room = form.cleaned_data['number_room']
            conference_room = form.cleaned_data['conference_room']
            gym = form.cleaned_data['gym']
            lunch = form.cleaned_data['lunch']
            breakfast = form.cleaned_data['breakfast']
            swimming_pool = form.cleaned_data['swimming_pool']
            internet = form.cleaned_data['internet']
            rate = request.POST.get('star')

            print("ostan")
            print(ostan)

            hotels = Hotel.objects.filter(ostan=ostan,conference_room=conference_room, gym=gym, lunch=lunch, breakfast=breakfast, swimming_pool=swimming_pool, internet= internet)
            #found_hotels = []
            #begin = datetime.datetime.combine(begin_form, datetime.time())
            #end = datetime.datetime.combine(end_form, datetime.time())

            return render(request, 'searchresults.html', {'hotels':hotels})

    else:
        form = Search()

    return render(request, 'searchresults.html', {'form':form})