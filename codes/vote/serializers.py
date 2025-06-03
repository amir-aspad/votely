from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Poll


class UserInfoSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile')

    class Meta:
        model = get_user_model()
        fields = ('username', 'profile_picture')


class ListingPollSerializer(serializers.ModelSerializer):
    creator = UserInfoSerializer(read_only=True)


    class Meta:
        model = Poll
        fields = ('id', 'title', 'end_time', 'start_time', 'creator')


class DetailPollSerializer(serializers.ModelSerializer):
    creator = UserInfoSerializer(read_only=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Poll
        fields = (
            'id', 'title', 'description', 'start_time', 'end_time', 'type',
            'is_active', 'count', 'creator'
        )


class PollActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('title', 'description', 'start_time', 'end_time', 'type', 'is_active')

    def create(self, validated_data):
        request = self.context['request']
        return Poll.objects.create(
            creator=request.user,
            **validated_data
        )
    
    def update(self, instance, validated_data):
        [setattr(instance, key, value) for key, value in validated_data.items()]
        instance.save()
        return instance

    def validate(self, data):
        s_t = data.get('start_time')
        e_t = data.get('start_time')

        if s_t and e_t and s_t>= e_t:
            raise serializers.ValidationError("Start time must be before end time.")
        return data

