from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HotelReservation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'UsersInformation.views.signin'),
    url(r'^usersign/', 'UsersInformation.views.Userregister'),
    url(r'^hotelsign/', 'UsersInformation.views.Hotelregister'),
    url(r'^useredit/', 'UsersInformation.views.UserEdit'),
    url(r'^home/','HotelsInformation.views.home'),
    url(r'^loginPage/', 'UsersInformation.views.signin'),
    url(r'^userEdit/', 'UsersInformation.views.UserEdit'),
    url(r'^userprofile/', 'UsersInformation.views.UserProfile'),
    url(r'^hotel/(?P<hotel_id>\d+)/$','HotelsInformation.views.hotel_viewer'),
    url(r'^myhotel/', 'UsersInformation.views.my_hotel'),
    url(r'^hoteledit/(?P<hotel_id>\d+)/$', 'UsersInformation.views.hotelEdit'),
    url(r'^error/', 'UsersInformation.views.hotelEdit'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/home/',}, name='logout'),
    url(r'^activation/', 'UsersInformation.views.activation'),
    url(r'^addhotel/', 'UsersInformation.views.AddHotel'),
    url(r'^hotelreserve/', 'HotelsInformation.views.Reserve'),
    url(r'^comment/','HotelsInformation.views.ajaxComment'),
)
