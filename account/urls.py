"""
Module that holds account app URLs.
"""
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserPasswordChangeView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("password-change/", UserPasswordChangeView.as_view(),
         name="password_change"),
]
