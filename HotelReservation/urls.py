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
    url(r'^error/', 'UsersInformation.views.eror'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/home/',}, name='logout'),
    url(r'^activation/', 'UsersInformation.views.activation'),
    url(r'^addhotel/', 'UsersInformation.views.AddHotel'),
    url(r'^hotelreserve/(?P<hotel_id>\d+)/$', 'HotelsInformation.views.reserve'),
    url(r'^comment/','HotelsInformation.views.ajaxComment'),
    url(r'^searchresults/','UsersInformation.views.search'),
    url(r'^hotelmanager/(?P<hotel_id>\d+)/$','HotelsInformation.views.manager'),
    url(r'^myadmin/','HotelsInformation.views.admin'),
    url(r'^hoteldelete/(?P<hotel_id>\d+)/$','HotelsInformation.views.hoteldelete'),
    url(r'^userdelete/(?P<user_id>\d+)/$','HotelsInformation.views.userdelete'),
    url(r'^usersee/(?P<user_id>\d+)/$','HotelsInformation.views.usersee'),
    url(r'^commentaccept/(?P<comment_id>\d+)/$','HotelsInformation.views.commentaccept'),
    url(r'^commentreject/(?P<comment_id>\d+)/$','HotelsInformation.views.commentreject'),
    url(r'^hotelaccept/(?P<hotel_id>\d+)/$','HotelsInformation.views.hotelaccept'),
    url(r'^bank/(?P<hotel_id>\d+)/$','HotelsInformation.views.payment'),
    url(r'^/(?P<hotel_id>\d+)/$','HotelsInformation.views.hotelaccept'),
    url(r'^adminpayment/','HotelsInformation.views.adminpayment'),

    url(r'^add_new_hotel/','HotelsInformation.views.add_new_hotel'),
    url(r'^add_new_room/','HotelsInformation.views.add_new_room'),
    url(r'^hotelBenefit/(?P<hotel_id>\d+)/$','HotelsInformation.views.hotelBenefit'),


)
