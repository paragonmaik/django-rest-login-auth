from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from account.serializers import UserRegistrationSerializer
from .renderers import UserRenderer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    """
    User Registration class with a post method
    """
    serializer_class = UserRegistrationSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request, format=None):
        """
        POST method that registers the user
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
