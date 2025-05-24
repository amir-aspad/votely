from rest_framework import serializers


class LoginUserSerializers(serializers.Serializer):
    info = serializers.CharField()
    password = serializers.CharField()