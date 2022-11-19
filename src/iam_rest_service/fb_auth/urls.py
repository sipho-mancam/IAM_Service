from django.urls import path
from . import views



urlpattern=[
    path('', views.login, name='fb_login')
]  