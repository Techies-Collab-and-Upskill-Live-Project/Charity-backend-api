from django.urls import path, re_path, include
from customauth.views import UserRegisterView,UserLoginView,UpdateProfileView,UserLogoutView,UserProfileView, PasswordResetView, DeleteUserView

urlpatterns = [
    path('register/', UserRegisterView.as_view({"post": "register"}, name='register')),
    path('login/', UserLoginView.as_view({"post": "login"}), name='login'),
    path('logout/', UserLogoutView.as_view({"post": "logout"}), name='logout'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
]