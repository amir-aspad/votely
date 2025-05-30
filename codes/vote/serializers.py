from rest_framework import serializers

from .models import Poll


class ListingPollSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username')
    creator_profile_picture = serializers.CharField(source='creator.profile.profile')
    count = serializers.IntegerField(read_only=True)


    class Meta:
        model = Poll
        fields = (
            'id', 'title', 'end_time', 'start_time', 'count',
            'creator_username', 'creator_profile_picture'
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
