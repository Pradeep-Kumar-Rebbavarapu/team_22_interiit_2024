from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
from rest_framework.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import datetime
from rest_framework.exceptions import NotFound

class MatchListAPI(ListAPIView):
    serializer_class = MatchInfoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = MatchInfo.objects.all().select_related(
            'team_a', 
            'team_b', 
            'meta', 
            'outcome'
        ).prefetch_related(
            'officials',
            'powerplays'
        )

        id = match_type = self.request.query_params.get('id', None)
        if id:
            queryset = queryset.filter(id = id)
 
        # Filter by match type (test/odi/t20)
        match_type = self.request.query_params.get('match_type', None)
        if match_type:
            queryset = queryset.filter(match_type=match_type)
            
        # Filter by team (searches in both team_a and team_b)
        team = self.request.query_params.get('team', None)
        if team:
            queryset = queryset.filter(
                Q(team_a__name__icontains=team) | 
                Q(team_b__name__icontains=team)
            )
            
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date or end_date:
            date_filters = Q()
            if start_date:
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                    date_filters &= Q(date__gte=start_date)
                except ValueError:
                    pass
            if end_date:
                try:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                    date_filters &= Q(date__lte=end_date)
                except ValueError:
                    pass
            queryset = queryset.filter(date_filters)
            
        # Filter by venue or city
        venue = self.request.query_params.get('venue', None)
        if venue:
            queryset = queryset.filter(venue__icontains=venue)
            
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__icontains=city)
            
        # Filter by gender
        gender = self.request.query_params.get('gender', None)
        if gender:
            queryset = queryset.filter(gender=gender)
            
        # Filter by season
        season = self.request.query_params.get('season', None)
        if season:
            queryset = queryset.filter(season=season)
            
        # Filter by player of match
        player = self.request.query_params.get('player_of_match', None)
        if player:
            queryset = queryset.filter(player_of_match__icontains=player)

        # Filter by target runs
        min_target = self.request.query_params.get('min_target', None)
        max_target = self.request.query_params.get('max_target', None)
        if min_target or max_target:
            target_filters = Q()
            if min_target:
                target_filters &= Q(target_runs__gte=min_target)
            if max_target:
                target_filters &= Q(target_runs__lte=max_target)
            queryset = queryset.filter(target_filters)

        # Filter by match outcome
        winner = self.request.query_params.get('winner', None)
        if winner:
            queryset = queryset.filter(outcome__winner__icontains=winner)
            
        # Order by date (newest first by default)
        order_by = self.request.query_params.get('order_by', '-date')
        if order_by not in ['date', '-date']:
            order_by = '-date'
        queryset = queryset.order_by(order_by)
        
        return queryset
    

class MatchPlayersAPI(RetrieveAPIView):
    serializer_class = MatchPlayersSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = MatchInfo.objects.all()
    lookup_field = 'id'

    def get_object(self):
        try:
            match = self.queryset.select_related(
                'team_a', 
                'team_b',
                'meta',
                'outcome'
            ).prefetch_related(
                'team_a__players',
                'team_b__players',
                'officials',
                'powerplays',
                'innings'
            ).get(id=self.kwargs['id'])
            return match
        except MatchInfo.DoesNotExist:
            raise NotFound(detail="Match not found")