from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signin, name='login'),
    path('', views.signin, name='login')
]