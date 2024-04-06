from django.urls import path
from .views import GoogleLoginApi

urlpatterns = [
      path("google/", GoogleLoginApi.as_view(), 
         name="login-with-google"),
]