"""
Module for users data serialization.
"""
from rest_framework import serializers
from account.models import User


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
        print(validated_data)
        # if validated_data.is_admin:
        #    return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializes user login data.
    """
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]
