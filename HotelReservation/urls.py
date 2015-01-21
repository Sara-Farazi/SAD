from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HotelReservation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^loginPage/', 'UsersInformation.views.signin'),
    url(r'^signup/', 'UsersInformation.views.Userregister'),
    url(r'^Hotelsignup/', 'UsersInformation.views.Hotelregister'),
    url(r'^userEdit/', 'UsersInformation.views.UserEdit'),
    url(r'^UserProfile/', 'UsersInformation.views.UserProfile'),
    url(r'^myhotel/', 'UsersInformation.views.my_hotel'),
    url(r'^edit/(?P<hotel_id>\d+)/$', 'UsersInformation.views.hotelEdit'),
    url(r'^error/', 'UsersInformation.views.hotelEdit'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/loginPage/',}, name='logout'),
    url(r'^activation/', 'UsersInformation.views.activation'),
)
