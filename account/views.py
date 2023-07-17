"""
Account views module.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from account.serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserPasswordChangeSerializer)
from .renderers import UserRenderer


def get_tokens_for_user(user):
    """
    Helper function for user token generation.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    """
    User Registration class with a post method.
    ...
    Methods:
        post(request):
            POST method for user registration.
    """
    serializer_class = UserRegistrationSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        """
        POST method for user registration.
        """

        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({"token": token, "message": "Registered!"},
                        status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    User Login class with a post method.
    ...
    Methods:
        post(request):
            POST method for user Login.
    """
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        """
        POST method for user Login.
        """
        serializer = UserLoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"errors": {"non_field_errors": ["Invalid Email or Password!"]}},
                            status=status.HTTP_404_NOT_FOUND)

        token = get_tokens_for_user(user)
        return Response({"token": token, "message": "Logged in!"}, status=status.HTTP_200_OK)


class UserPasswordChangeView(APIView):
    """
    User password change class with a post method.
    ...
    Methods:
        post(request, format):
            POST method for password change.
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """
        POST method for user password change.
        """
        print("------------", request.user)
        serializer = UserPasswordChangeSerializer(
            data=request.data, context={"user": request.user})
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Password was changed successfully."},
                        status=status.HTTP_200_OK)
