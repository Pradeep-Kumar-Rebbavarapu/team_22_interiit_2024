from rest_framework import generics
from .serializers import MatchSerializer, MatchDetailSerializer
from .models import MatchInfo

from django_filters.rest_framework import DjangoFilterBackend


class MatchList(generics.ListCreateAPIView):
    serializer_class = MatchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_a', 'team_b', 'city', 'date', 'venue', 'match_type', 'season', 'date', 'gender', 'season']
    ordering_fields = ['date']
    ordering = ['date']

    def get_queryset(self):
        queryset = MatchInfo.objects.all()
        limit = self.request.query_params.get('limit', '20')
        if limit is not None and limit.isdigit():
            queryset = queryset[:int(limit)]
        return queryset


class MatchDetail(generics.RetrieveUpdateAPIView):
    queryset = MatchInfo.objects.all()
    serializer_class = MatchDetailSerializer
