from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('register', views.Registration, name='register'),
    path('login', views.LoginView, name='login'),
    path('logout', views.LogoutView, name='logout'),
]