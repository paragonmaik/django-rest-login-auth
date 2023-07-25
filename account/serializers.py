"""
Module for users data serialization.
"""
from rest_framework import serializers
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.models import User
from account.utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializes user registration data.
    ...
    Methods:
        validate(attrs):
            Validates if password and password2 fields are a match.

        create(validated_data):
            Creates user with the validated data.
    """
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "password",
                  "password2", "terms_conditions", "is_admin"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "Passwords do not match!")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializes user login data.
    """
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    """
    Serializes user password change data.
    ...
    Methods:
        validate(attrs):
            Validates if password and password2 fields are a match.
    """
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = self.context.get("user")

        if not user:
            raise serializers.ValidationError("Unauthenticated User!")

        if password != password2:
            raise serializers.ValidationError(
                "Passwords do not match!")

        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    """
    Serializes password reset email.
    ...
    Methods:
        validate(attrs):
            Validates if email is valid.
    """
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "If the given email belongs to a user, a reset link will be sent.")

        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        link = "http://localhost:8000/api/user/reset/" + uid + token

        data = {
            "subject": "Password reset.",
            "body": "Click in the following link to reset your password: " + link,
            "receiver_email": user.email
        }

        Util.send_email(data)

        return attrs


class UserPasswordResetSerializer(serializers.ModelSerializer):
    """
    Serializes password reset data.
    ...
    Methods:
        validate(attrs):
            Validates if password and password2 fields are a match.
    """
    class Meta:
        model = User
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        uid = self.context.get("uid")
        token = self.context.get("token")

        if uid is None or token is None:
            raise serializers.ValidationError("Unexpected Error!")

        if password != password2:
            raise serializers.ValidationError(
                "Passwords do not match!")

        user_id = smart_str(urlsafe_base64_encode(uid))
        user = User.objects.get(id=user_id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Token has expired.")

        user.set_password(password)
        user.save()

        return attrs
