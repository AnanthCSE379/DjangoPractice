from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.myView,name='myview'),
    # Required exam URLs (no trailing slash).
    path('buildingapp/home', views.home, name='home'),
    path('buildingapp/registerFlat', views.register_flat, name='register_flat'),
    path('buildingapp/dispApartment', views.display_apartments, name='display_apartments'),
    path('buildingapp/dispRegistration', views.display_registrations,
         name='display_registrations'),
    # Extra URLs complete customer CRUD and display a specific receipt.
    path('buildingapp/receipt/<int:pk>', views.receipt, name='receipt'),
    path('buildingapp/editRegistration/<int:pk>', views.edit_registration,
         name='edit_registration'),
    path('buildingapp/deleteRegistration/<int:pk>', views.delete_registration,
         name='delete_registration'),
]
