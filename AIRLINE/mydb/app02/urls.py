from django.urls import path
from app02 import views

urlpatterns = [
    path('',views.welcome),
    path('welcome/',views.welcome),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('index/',views.index),
    path('logouot/',views.logout,name='logout'),
    path('information/',views.information),
    path('passenger/',views.passenger),
    path('add_passenger/',views.add_passenger),
    path('delete_passenger/',views.delete_passenger),
    path('search/',views.flights_search),
    path('search_result/',views.search_result),
    path('booking/',views.book),
    path('booking_success/',views.booking_success),
    path('order_list/',views.order_list),
    path('refunding/',views.refund),
    path('home_not/',views.home_not),
    path('help/',views.help),
    path('help_not/',views.help_not),
]