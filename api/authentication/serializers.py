from django.contrib.auth.base_user import AbstractBaseUser
from django.http import response
from .models import User
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should only contain alphanumeric characters"
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    # this is the field that will be in the swagger form
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=68, min_length=6, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "tokens"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Ivalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed(
                "Account is not active, please contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens,
        }


class RequestPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    uidb64 = serializers.ReadOnlyField()
    token = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['email', 'uidb64', 'token']

    def validate(self, attrs):
        email = attrs.get("email", "")
        user = User.objects.filter(email=email)
        if not user.exists():
            raise serializers.ValidationError('Email does not exist', 400)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.first().id))
        token = PasswordResetTokenGenerator().make_token(user.get())
        return {
            "email": email,
            "uidb64": uidb64,
            "token": token
        }


class PasswordTokenCheckSerializer(serializers.ModelSerializer):
    uidb64 = serializers.CharField(
        min_length=1)
    token = serializers.CharField(
        min_length=1)

    class Meta:
        model = User
        fields = ['uidb64', 'token']

    def validate(self, attrs):
        try:
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            error = AuthenticationFailed(
                'Token is not valid, please request a new one')
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise error
            return {
                'uidb64': uidb64,
                'token': token}
        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise error


class SetNewPasswordSerilizer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
            return user

        except Exception:
            raise AuthenticationFailed('The reset link is invalid', 401)
