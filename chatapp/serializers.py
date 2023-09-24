from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import Message
from .models import User
from .models import Chat


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=False, allow_blank=False)
    email = serializers.CharField(allow_blank=False, allow_null=False)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()
        user = User.objects.filter(email=attrs['email']).first()
        if user:
            if user.is_active:
                raise ValidationError(
                    {'detail': 'User with this email already exists.'}
                )
            else:
                attrs['is_active'] = True
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(allow_null=False, allow_blank=False)
    password = serializers.CharField(allow_blank=False, allow_null=False, min_length=6)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                return user
            raise serializers.ValidationError(
                {"error": "Invalid credentials"}
            )
        raise serializers.ValidationError(
            {"error": "Username and password are required"}
        )


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['chat_sender', 'chat_recipient']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'message_sender', 'message_recipient', 'content', 'timestamp']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
