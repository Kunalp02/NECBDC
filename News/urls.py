from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.display_news, name="display_news"),
]
    