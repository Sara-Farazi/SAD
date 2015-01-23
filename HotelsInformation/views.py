from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.
from HotelsInformation.models import Hotel, Comment


# Create your views here.


def home(request):
    return render(request, 'home.html')

def hotel_viewer(request, hotel_id):
    hotel_id = int(hotel_id)
    hotel = Hotel.objects.get(id=hotel_id)
    comment = Comment.objects.filter(hotel=hotel,status=1)
    return render(request, 'HotelProfile.html', {'hotel': hotel, 'comment': comment})

def Reserve(request):
     return render(request,'hotelreserve.html')


def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
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
        new_cm = Comment(body=body, user=user, name=user.username, email=user.email, status=0, hotel=hotel,
                         date=datetime.datetime.now())
        new_cm.save()
        return {
            'status':'ok'
        }


    return HttpResponse(status=400)