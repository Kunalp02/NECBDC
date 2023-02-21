from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('loginUser/', views.loginUser, name='loginUser'),
    path('signupUser/', views.signupUser, name='signupUser'),
    path('logOut/', views.logOut, name='logOut'),
    
]
    