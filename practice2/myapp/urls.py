from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.startpage,name="startpage"),
    path('register/', views.register,name="register"),
    path('display/', views.display,name="display"),
    path('payment/', views.payment,name="payment"),
]
