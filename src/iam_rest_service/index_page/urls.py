from django.urls import path
from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.email_login, name='login'),
    path('signup', views.email_sign_up, name='sign-up'),
    path('google/signup', views.g_signup, name='gSignup'),
]