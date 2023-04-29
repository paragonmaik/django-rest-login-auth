from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserRegistrationView(APIView):
    """
    placeholder docstring
    """

    def register(self, request, format=None):
        return Response({"message": "test"}, status=status.HTTP_201_CREATED)
