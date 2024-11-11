from rest_framework import serializers
from .models import Player, Team, Match, OptimalTeam, Delivery

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = '__all__'

class OptimalTeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    
    class Meta:
        model = OptimalTeam
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)
    optimal_teams = OptimalTeamSerializer(many=True, read_only=True)
    deliveries = DeliverySerializer(many=True, read_only=True)
    
    class Meta:
        model = Match
        fields = '__all__'

