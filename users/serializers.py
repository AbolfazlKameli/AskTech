from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse

from .models import User
from utils import JWT_token, send_email


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
        print('=' * 90)
        print(validated_data)
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        token = JWT_token.generate_token(user)
        link = request.build_absolute_uri(
            reverse('users:user_register_verify', kwargs={'token': token['token']})
        )
        send_email.send_link(email, link)
        return user

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
