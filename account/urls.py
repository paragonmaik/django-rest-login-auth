"""
Module that holds account app URLs.
"""
from django.urls import path
from .views import (UserRegistrationView, UserLoginView,
                    UserPasswordChangeView, SendPasswordResetEmailView, UserPasswordResetView)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("password-change/", UserPasswordChangeView.as_view(),
         name="password_change"),
    path("send-reset-password-email/", SendPasswordResetEmailView.as_view(),
         name="send_reset_password_email"),
    path("reset-password/<uid>/<token>/",
         UserPasswordResetView.as_view(), name="reset_password")
]
