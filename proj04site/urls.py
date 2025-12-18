from django.contrib import admin
from django.urls import path
from webinterface import views

urlpatterns = [
    path('', views.index, name='controller'),
]
