from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('',views.display,name='list'),
    path('add/',views.register,name='add'),
    path('<int:pk>/delete/',views.delete,name='delete'),
]
