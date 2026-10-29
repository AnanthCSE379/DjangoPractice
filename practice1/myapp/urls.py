from django.urls import path
from . import views

urlpatterns = [
    path('',views.start,name='start'),
    path('register/',views.register,name='register'),
    path('findbest/',views.findbest,name='findbest'),
    path('searchplayer/',views.searchplayer,name='searchplayer'),
    path('displayplayer/',views.display,name='display'),
]
