from django.contrib.auth import authenticate
from django.db.models import Count, Sum
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.
from HotelsInformation.models import Hotel, Comment, MyUser, Reserve, HotelRoom, RoomType


# Create your views here.
from UsersInformation.forms import reserveForm


def home(request):
    return render(request, 'home.html')


def hotelBenefit(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)

    reserve1 = Reserve.objects.filter(hotel=hotel).values('type').annotate(dcount=Sum('number'), ccount=Sum('payment'))
    #reserve2 = Reserve.objects.all().values('type').annotate(dcount=Sum('payment'))
    return render(request, 'benefit.html', {'reserve1': reserve1})



def admin(request):
    hotels = Hotel.objects.filter(is_accepted=True)
    notacceptedhotels = Hotel.objects.filter(is_accepted=False)
    reserves = Reserve.objects.all().values('hotel').annotate(dcount=Sum('payment'))
    users = MyUser.objects.all()
    comments = Comment.objects.all()


    benefit = []
    for res in reserves:
        benefit.append(res['dcount'] * 0.3)

    print(benefit)
    benefit.reverse()
    print(benefit)
    return render(request, 'myadmin.html', {'reserves': reserves, 'hotels': hotels, 'notacceptedhotels': notacceptedhotels,'comments': comments, 'users' : users, 'benyamin': benefit})


def manager(request, hotel_id):
    hotel_id = int(hotel_id)
    hotel = Hotel.objects.get(id=hotel_id)
    comment = Comment.objects.filter(hotel=hotel,status=1)
    return render(request, 'hotelmanager.html', {'hotel': hotel, 'comment': comment})









def hotel_viewer(request, hotel_id):
    is_able_comment = False
    hotel_id = int(hotel_id)
    hotel = Hotel.objects.get(id=hotel_id)

    rooms = HotelRoom.objects.filter(hotel=hotel)
    room_type =[]
    for room in rooms:
        if room.type not in room_type:
            room_type.append(room.type)


    #rooms = RoomType.objects.filter(hotel=hotel)
    #print(rooms)
    print(room_type)
    reserves = Reserve.objects.filter(user=request.user)
    for reserve in reserves:
        if reserve.hotel==hotel:
            is_able_comment = True
    print(is_able_comment)
    comment = Comment.objects.filter(hotel=hotel,status=1)
    if hotel.is_accepted==True:
        return render(request, 'HotelProfile.html', {'hotel': hotel, 'comment': comment, 'is_able_comment':is_able_comment,'type':room_type})
    else:
        return render(request, 'home.html')

def reserve(request, hotel_id):
    hotel = Hotel.objects.get(id = hotel_id)
    rooms = HotelRoom.objects.filter(hotel=hotel)
    return render(request,'hotelreserve.html', {'rooms' : rooms, 'hotel':hotel})

#def payment(request, hotel_id):
#    if request.method == 'POST':
#        form = reserveForm(request.POST)
#        print("payment not valid")
#        if form.is_valid():
#            print("payment")
#            #user = MyUser.objects.get(id = request.user.pk)
#            username = form.cleaned_data['username']
#            password = form.cleaned_data['password']
#            user = authenticate(username=username, password=password)
#            hotel = Hotel.objects.get(id = hotel_id)
#            rooms = HotelRoom.objects.filter(hotel=hotel)
#            for room in rooms:
#                type = request.POST.getlist('roomType')
#                if type:
#                    print(type)
#                    print("i got a type")
#                    number = form.cleaned_data['numberOfRooms']
#                    typeRooms = HotelRoom.objects.filter(hotel=hotel, type=type, is_reserved=False)
#                    print(typeRooms)
#                    print(typeRooms.count())
#                    if typeRooms.count() >= number:
#                        print("Im here!")
#                        for i in number:
#                            typeRooms[i].is_reserved = True
#
#
#                        newReserve = Reserve.objects.create(user=user, hotel=hotel, payment=room.cost*number)
#                        newReserve.save()
#                        return HttpResponseRedirect("/success/")
#
#
#                    else:
#                        return HttpResponseRedirect("/error/")
#
#
#    else:
#        form = reserveForm()
#
#    return render(request, 'bank.html',{'form': form})





def json_serialize(obj):
    if isinstance(obj, Hotel):
        return {
            'id': obj.id,
            'hotel_name': obj.first_name,
            'address': obj.last_name,
            'email': obj.email,
            'phone': obj.phone
        }
    if isinstance(obj, set) or isinstance(obj, QuerySet):
        return list(obj)
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, list):
        return obj

    return {}


def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is
    added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects, default=json_serialize)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except Exception as e:
            print (e)
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator

@csrf_exempt
@json_response
def ajaxComment(request):
    if request.method=="POST":
        body = request.POST.get('cm_body')
        id = int(request.POST.get('hotel_id'))
        hotel = Hotel.objects.get(id=id)
        user = request.user
        rate = request.POST.get('star')
        hotel.given_rate = rate
        hotel.save()

        new_cm = Comment(body=body, user=user, name=user.username, email=user.email, status=0, hotel=hotel,
        date=datetime.datetime.now())
        new_cm.save()
        return {
            'status':'ok'

                }

    return HttpResponse(status=400)

def hoteldelete(request,hotel_id):
  hotel_id = int(hotel_id)
  hotel = Hotel.objects.get(id=hotel_id).delete()
  hotels = Hotel.objects.filter(is_accepted=True)
  users = MyUser.objects.all()
  comments = Comment.objects.all()
  notacceptedhotels = Hotel.objects.filter(is_accepted=False)
  return render(request,'myadmin.html', {'hotels': hotels,'notacceptedhotels':notacceptedhotels, 'comments': comments, 'users' : users})


def userdelete(request,user_id):
   user_id = int(user_id)
   user = MyUser.objects.get(id=user_id).delete()
   hotels = Hotel.objects.filter(is_accepted=True)
   users = MyUser.objects.all()
   comments = Comment.objects.all()
   notacceptedhotels = Hotel.objects.filter(is_accepted=False)
   return render(request,'myadmin.html', {'hotels': hotels,'notacceptedhotels':notacceptedhotels, 'comments': comments, 'users' : users})

def usersee(request, user_id):
    user = MyUser.objects.get(id=user_id)
    return render(request,'userprofile.html' ,{'user':user})


def commentaccept(request,comment_id):

    comment_id = int(comment_id)
    comment =Comment.objects.get(id=comment_id)
    comment.status=1
    comment.save()
    hotels = Hotel.objects.filter(is_accepted=True)
    users = MyUser.objects.all()
    comments = Comment.objects.all()
    notacceptedhotels = Hotel.objects.filter(is_accepted=False)
    return render(request,'myadmin.html', {'hotels': hotels,'notacceptedhotels':notacceptedhotels, 'comments': comments, 'users' : users})


def commentreject(request,comment_id):

    comment_id = int(comment_id)
    comment =Comment.objects.get(id=comment_id)
    comment.status=2
    comment.save()
    comment = Comment.objects.get(id=comment_id).delete()

    hotels = Hotel.objects.filter(is_accepted=True)
    users = MyUser.objects.all()
    comments = Comment.objects.all()
    notacceptedhotels = Hotel.objects.filter(is_accepted=False)
    return render(request,'myadmin.html', {'hotels': hotels,'notacceptedhotels':notacceptedhotels, 'comments': comments, 'users' : users})


def hotelaccept(request, hotel_id):
    hotel_id = int(hotel_id)
    hotel = Hotel.objects.get(id = hotel_id)
    hotel.is_accepted = True
    hotel.save()
    hotels = Hotel.objects.filter(is_accepted=True)
    notacceptedhotels = Hotel.objects.filter(is_accepted=False)
    users = MyUser.objects.all()
    comments = Comment.objects.all()

    return render(request,'myadmin.html', {'hotels': hotels, 'notacceptedhotels': notacceptedhotels,'comments': comments, 'users' : users})

def adminpayment(request):
    reserve=Reserve.objects.values('hotel').annotate(dcount=Count('payment'))
    print(reserve)
    return render(request,'myadmin.html',{'reserve':reserve})


def str_to_bool(s):
    if s == 'true':
         return True
    elif s == 'false':
         return False



@csrf_exempt
@json_response
def add_new_hotel(request):
    if request.method=="POST":
        name = request.POST.get('hotel_name')
        addr = request.POST.get('addr')
        star = request.POST.get('star')
        phone = request.POST.get('phone')
        ostan = request.POST.get('ostan')
        email = request.POST.get('email')

        breakfast = str_to_bool(request.POST.get('breakfast'))
        lunch = str_to_bool(request.POST.get('lunch'))
        gym = str_to_bool(request.POST.get('gym'))
        internet = str_to_bool(request.POST.get('internet'))
        conf = str_to_bool(request.POST.get('conference_room'))
        pool = str_to_bool(request.POST.get('swimming_pool'))

        hotel = Hotel.objects.create(hotel_name=name, ostan=ostan, address=addr,
                                     hotel_phone=phone, hotel_email=email, hotel_owner=request.user,
                                     hotel_rate=star, gym=gym,conference_room=conf, lunch=lunch,breakfast=breakfast,
                                     swimming_pool=pool, internet=internet, capacity=0, is_accepted=False)
        hotel.save()
    return {
        'status':'Ok!',
        'id': hotel.id
    }

@csrf_exempt
@json_response
def add_new_room(request):
    if request.method=="POST":
        id = request.POST.get('id')
        view = request.POST.get('view')
        number = int(request.POST.get('number'))
        capacity = request.POST.get('capacity')
        metraj = request.POST.get('metraj')
        cost = request.POST.get('cost')
        type = request.POST.get('type')

        hotel = Hotel.objects.get(id=id)
        room_type = RoomType.objects.get_or_create(numberOfType=number)
        for i in range(number):
            room = HotelRoom.objects.create(roomNumber=i, hotel=hotel, metraj=metraj,
                                             view=view, is_reserved=False, capacity=capacity,
                                             type=type, numberOfType=number, cost=cost)
            room.save()

    return {
        'status': 'Ok!',
    }


def payment(request, hotel_id):
    if request.method == 'POST':
        form = reserveForm(request.POST)
        print("payment not valid")
        if form.is_valid():
            print("valid")
            type = str_to_bool(request.POST.get('roomType'))
            hotel = Hotel.objects.get(id = hotel_id)
            rooms = HotelRoom.objects.filter(hotel = hotel)
            for room in rooms:
                if room.type==type:
                    if room.is_reserved:
                        return HttpResponseRedirect("/error/")
                    else:
                        room.is_reserved=True
                        room.save()
                        print("reserved")
                        return render(request, 'bank.html',{'form': form})

    else:
       form = reserveForm()

    return render(request, 'bank.html',{'form': form})
