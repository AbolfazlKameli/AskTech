from django.contrib.auth.password_validation import validate_password
from django.urls import reverse
from rest_framework import serializers

from utils import JWT_token, send_email
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        email = validated_data.get("email")
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        token = JWT_token.generate_token(user)
        link = request.build_absolute_uri(
            reverse('users:user_register_verify', kwargs={'token': token['token']})
        )
        send_email.send_link(email, link)
        return {'id': user.id, 'username': user.username, 'email': user.email}

    def validate(self, data):
        password1 = data.get('password')
        password2 = data.get('password2')
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError('Passwords must match')
        try:
            validate_password(password2)
        except serializers.ValidationError:
            raise serializers.ValidationError()
        return data


class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': 'User does not exist!'})
        if user.is_active:
            raise serializers.ValidationError({'error': 'Account already activated'})
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_new_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise serializers.ValidationError({'error': 'Passwords must match'})
        try:
            validate_password(new_password)
        except serializers.ValidationError:
            raise serializers.ValidationError()
        return attrs


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')
        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise serializers.ValidationError('Passwords must match')
        try:
            validate_password(new_password)
        except serializers.ValidationError:
            raise serializers.ValidationError()
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ('id', 'last_login', 'is_superuser', 'is_admin', 'groups', 'user_permissions')

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError('fields can not be blank.')
        return attrs

    def validate_username(self, username):
        users = User.objects.filter(username__exact=username)
        if users.exists():
            raise serializers.ValidationError('user with this username already exists.')
        return username

    def validate_email(self, email):
        users = User.objects.filter(email__exact=email)
        if users.exists():
            raise serializers.ValidationError('user with this Email already exists.')
        return email
