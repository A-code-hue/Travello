from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),

    # CRUD: Destinations
    path('destinations/', views.destination_list, name='admin_destination_list'),
    path('destinations/create/', views.destination_create, name='admin_destination_create'),
    path('destinations/edit/<int:pk>/', views.destination_edit, name='admin_destination_edit'),
    path('destinations/delete/<int:pk>/', views.destination_delete, name='admin_destination_delete'),
]
