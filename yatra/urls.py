from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Home & Static Pages
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
 
    # Authentication
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    # Destinations & Details
    path('destination_list/<str:city>/', views.destination_list, name='destination_list'),
    path('destination_list/destination_details/<str:destination_name>', views.destination_details, name='destination_details'),

    # Passenger Details & Payment
    path('passenger_detail/<str:city_name>/', views.pessanger_detail_def, name='pessanger_detail_def'),
    path('initiate/', views.initiate_payment, name='initiate'),
    path('verify/', views.verify_payment, name='verify_payment'),

    # Recommendations
    path('recommend', views.get_recommendations, name='recommendations'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),

    
    # User bookings and GPS update
    path('bookings/', views.user_booking_list, name='user_booking_list'),
    path('bookings/cancel/<int:trip_id>/', views.cancel_booking, name='cancel_booking'),
    path('bookings/update-location/<int:trip_id>/', views.update_booking_location, name='update_booking_location')
]
