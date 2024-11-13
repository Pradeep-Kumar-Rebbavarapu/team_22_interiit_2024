from rest_framework import generics
from .serializers import MatchSerializer, ChatSerializer, MessageSerializer
from .models import MatchInfo, Chat, Message

from django_filters.rest_framework import DjangoFilterBackend


class MatchList(generics.ListCreateAPIView):
    serializer_class = MatchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_a', 'team_b', 'city', 'date', 'venue', 'match_type', 'season', 'date', 'gender', 'season','id']
    ordering_fields = ['date']
    ordering = ['date']

    def get_queryset(self):
        queryset = MatchInfo.objects.all()
        limit = self.request.query_params.get('limit')
        if limit is not None and limit.isdigit():
            queryset = queryset[:int(limit)]
        return queryset


class ChatList(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatDetail(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    lookup_field = 'match'
    serializer_class = ChatSerializer
