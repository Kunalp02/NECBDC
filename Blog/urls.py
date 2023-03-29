from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('post_detail/<slug:slug>', views.post_detail, name='post_detail')
]


