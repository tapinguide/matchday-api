
from rest_framework import serializers
from .models import Competition, Club, Match, MatchStatus, Event, MustReadWatch, ContextBlurb

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'

class MatchStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchStatus
        fields = '__all__'

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'

class ClubWithCrestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        depth = 1
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        depth = 2
        fields = '__all__'

class ActiveMatchSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    class Meta:
        model = Match
        depth = 2
        fields = '__all__'

class MustReadWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MustReadWatch
        fields = '__all__'

class ContextBlurbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContextBlurb
        fields = '__all__'
