from rest_framework import serializers
from .models import Challenge, UserChallenge

class ChallengeSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField() 

    class Meta:
        model = Challenge
        fields = [
            'id',
            'title',
            'description',
            'prompt',
            'category',
            'points',      
            'is_active',
            'completed',
            'hint_1',
            'hint_2',
            'hint_3',
        ]

    def get_points(self, obj):
        return obj.current_points

    def get_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserChallenge.objects.filter(user=request.user, challenge=obj).exists()
        return False


class UserChallengeSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer(read_only=True)

    class Meta:
        model = UserChallenge
        fields = ['challenge', 'completed_at', 'awarded_points'] 
