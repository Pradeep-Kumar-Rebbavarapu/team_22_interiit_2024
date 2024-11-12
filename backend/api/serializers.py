from rest_framework import serializers
from .models import MatchInfo, Team, MetaData, Official, Outcome, Inning, Delivery, Over, Extra, Wicket, Powerplay, Player

class OfficialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Official
        fields = "__all__"

# Meta information serializer
class MetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields = "__all__"

# Team serializer
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

# Outcome serializer
class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = "__all__"

# Extra serializer
class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = "__all__"

# Wicket serializer
class WicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wicket
        fields = "__all__"

# Delivery serializer
class DeliverySerializer(serializers.ModelSerializer):
    extras = ExtraSerializer()
    wickets = WicketSerializer(many=True)

    class Meta:
        model = Delivery
        fields = "__all__"

# Over serializer
class OverSerializer(serializers.ModelSerializer):
    deliveries = DeliverySerializer(many=True)

    class Meta:
        model = Over
        fields = "__all__"

# Innings serializer
class InningsSerializer(serializers.ModelSerializer):
    overs = OverSerializer(many=True)

    class Meta:
        model = Inning
        fields = "__all__"

# PowerPlay serializer
class PowerPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Powerplay
        fields = "__all__"

# Match serializer
class MatchSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    outcome = OutcomeSerializer()

    class Meta:
        model = MatchInfo
        fields = "__all__"

# Match Detail serializer
class MatchDetailSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    outcome = OutcomeSerializer()
    innings = InningsSerializer(many=True)
    powerplays = PowerPlaySerializer(many=True)

    class Meta:
        model = MatchInfo
        fields = "__all__"

# Match Players serializer
class MatchPlayersSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    meta = MetaDataSerializer()
    officials = OfficialSerializer(many=True)
    outcome = OutcomeSerializer()
    powerplays = PowerPlaySerializer(many=True)
    innings = InningsSerializer(many=True)

    class Meta:
        model = MatchInfo
        fields = "__all__"


