from rest_framework import serializers
from .models import MatchInfo, Team, MetaData, Official, Outcome, Inning, Delivery, Over, Extra, Wicket, Powerplay, Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'unique_name', 'identifier']


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = '__all__'


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class OverSerializer(serializers.ModelSerializer):
    deliveries = DeliverySerializer(many=True)
    class Meta:
        model = Over
        fields = '__all__'


class InningsSerializer(serializers.ModelSerializer):
    overs = OverSerializer(many=True)
    class Meta:
        model = Inning
        fields = '__all__'


class PowerPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Powerplay
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    outcome = OutcomeSerializer()
    
    class Meta:
        model = MatchInfo
        fields = '__all__'


class MatchDetailSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    outcome = OutcomeSerializer()
    innings = InningsSerializer(many=True)
    powerplays = PowerPlaySerializer(many=True)
    
    class Meta:
        model = MatchInfo
        fields = '__all__'

