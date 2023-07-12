"""
Module that holds account app URLs.
"""
from django.urls import path
from .views import UserRegistrationView, UserLoginView, AdminRegistrationView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("register/admin/", AdminRegistrationView.as_view(), name="register_admin"),
    path("login/", UserLoginView.as_view(), name="login"),
]
