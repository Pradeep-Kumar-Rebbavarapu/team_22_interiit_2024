from rest_framework import serializers
from .models import MatchInfo, Team, MetaData, Official, Outcome, Inning, Delivery, Over, Extra, Wicket, Powerplay, Player, Message, Chat

# Official serializer
class OfficialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Official
        fields = "__all__"

# Meta information serializer
class MetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields = "__all__"

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id","identifier","name","role"]

# Team serializer
class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)  # Adding players field
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

# Player serializer


# Match serializer
class MatchSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    team_a_players = PlayerSerializer(many=True)
    team_b_players = PlayerSerializer(many=True)
    class Meta:
        model = MatchInfo
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj:Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ["pk", "name", "messages", "last_message"]
        depth = 1
        read_only_fields = ["messages", "last_message"]

    def get_last_message(self, obj:Chat):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data
