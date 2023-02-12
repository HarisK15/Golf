from django.contrib import admin
from django.urls import path
from records import views

urlpatterns = [
    path('log-in/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log-out/', views.log_out, name='log_out'),
    path('', views.dashboard, name='home'),

]