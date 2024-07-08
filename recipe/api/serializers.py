from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# https://medium.com/mozilla-firefox-club/register-login-and-logout-in-django-rest-framework-using-jwt-a49963dfddce
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError("The username should only contain alphanumeric characters")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data) # case when email or username isn't unique?

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj["username"])
        return {
            "refresh": user.tokens()['refresh'],
            "access": user.tokens()['access']
            }
    class Meta:
        model = User
        fields = ["username", "password", "tokens"]
    def validate(self, attrs):
        username = attrs.get("username", "")
        password = attrs.get("password", "")

        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")

        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens
        }
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get("refresh")
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("Token is invalid or expired")