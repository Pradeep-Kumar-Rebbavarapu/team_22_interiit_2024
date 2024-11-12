from rest_framework.serializers import ModelSerializer
from .models import MetaData,Team,Official,Outcome,Powerplay,MatchInfo, Inning

class MetaDataSerializer(ModelSerializer):
    class Meta:
        model = MetaData
        fields = '__all__'

class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class OfficialSerializer(ModelSerializer):
    class Meta:
        model = Official
        fields = '__all__'

class OutcomeSerializer(ModelSerializer):
    class Meta:
        model = Outcome
        fields = '__all__'

class PowerplaySerializer(ModelSerializer):
    class Meta:
        model = Powerplay
        fields = '__all__'

class MatchInfoSerializer(ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    meta = MetaDataSerializer()
    officials = OfficialSerializer(many=True)
    outcome = OutcomeSerializer()
    powerplays = PowerplaySerializer(many=True)

    class Meta:
        model = MatchInfo
        fields = '__all__'

class InningSerializer(ModelSerializer):
    class Meta:
        model = Inning
        fields = '__all__'

class MatchPlayersSerializer(ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    meta = MetaDataSerializer()
    officials = OfficialSerializer(many=True)
    outcome = OutcomeSerializer()
    powerplays = PowerplaySerializer(many=True)
    innings = InningSerializer(many=True)

    class Meta:
        model = MatchInfo
        fields = '__all__'