from django.contrib import admin
from django.urls import path
from student import views
urlpatterns=[
     path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]