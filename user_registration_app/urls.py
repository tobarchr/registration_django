from django.urls import path
from . import views 

urlpatterns = [
    path('',views.index),
    path('success',views.success_screen),
    path('registration',views.registration),
    path('login',views.login),
    path('logoff',views.logoff)
]