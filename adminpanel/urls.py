from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),

    # User Management
    path('users/', views.user_list, name='admin_user_list'),
    path('users/create/', views.user_create, name='admin_user_create'),
    path('users/edit/<int:pk>/', views.user_edit, name='admin_user_edit'),
    path('users/delete/<int:pk>/', views.user_delete, name='admin_user_delete'),

    # City
    path('cities/', views.city_list, name='admin_city_list'),
    path('cities/create/', views.city_create, name='admin_city_create'),
    path('cities/edit/<int:pk>/', views.city_edit, name='admin_city_edit'),
    path('cities/delete/<int:pk>/', views.city_delete, name='admin_city_delete'),

    # Destination
    path('destinations/', views.destination_list, name='admin_destination_list'),
    path('destinations/create/', views.destination_create, name='admin_destination_create'),
    path('destinations/edit/<int:pk>/', views.destination_edit, name='admin_destination_edit'),
    path('destinations/delete/<int:pk>/', views.destination_delete, name='admin_destination_delete'),

    # DetailedDescription
    path('details/', views.detail_list, name='admin_detail_list'),
    path('details/create/', views.detail_create, name='admin_detail_create'),
    path('details/edit/<int:pk>/', views.detail_edit, name='admin_detail_edit'),
    path('details/delete/<int:pk>/', views.detail_delete, name='admin_detail_delete'),

    # PassengerDetail
    path('passengers/', views.passenger_list, name='admin_passenger_list'),
    path('passengers/create/', views.passenger_create, name='admin_passenger_create'),
    path('passengers/edit/<int:pk>/', views.passenger_edit, name='admin_passenger_edit'),
    path('passengers/delete/<int:pk>/', views.passenger_delete, name='admin_passenger_delete'),

    # Transaction
    path('transactions/', views.transaction_list, name='admin_transaction_list'),
    path('transactions/create/', views.transaction_create, name='admin_transaction_create'),
    path('transactions/edit/<int:pk>/', views.transaction_edit, name='admin_transaction_edit'),
    path('transactions/delete/<int:pk>/', views.transaction_delete, name='admin_transaction_delete'),

    # Newsletter
    path('newsletters/', views.newsletter_list, name='admin_newsletter_list'),
    path('newsletters/delete/<int:pk>/', views.newsletter_delete, name='admin_newsletter_delete'),

    # Contact URLs
    path('contacts/', views.contact_list, name='admin_contact_list'),
    path('contacts/delete/<int:pk>/', views.contact_delete, name='admin_contact_delete'),

    # BlogPost URLs
    path('blogposts/', views.blogpost_list, name='admin_blogpost_list'),
    path('blogposts/create/', views.blogpost_create, name='admin_blogpost_create'),
    path('blogposts/edit/<int:pk>/', views.blogpost_edit, name='admin_blogpost_edit'),
    path('blogposts/delete/<int:pk>/', views.blogpost_delete, name='admin_blogpost_delete'),

    # Admin booking management
    path('bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('bookings/approve/<int:trip_id>/', views.admin_approve_booking, name='admin_approve_booking'),
    path('bookings/cancel/<int:trip_id>/', views.admin_cancel_booking, name='admin_cancel_booking'),
]
