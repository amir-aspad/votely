from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from utils.validations import validate_phone


class LoginUserSerializer(serializers.Serializer):
    info = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RegisterUserSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[validate_phone])
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.get('confirm_password')

        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')
        
        return attrs
        
    def validate_phone(self, value):
        User = get_user_model()

        if User.objects.filter(phone=value).exists():
            raise ValidationError('this phone is already exists')
    
        return value