from django.contrib import admin
from django.urls import path
from registrationandemail import views
urlpatterns=[
     path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email')
]

    