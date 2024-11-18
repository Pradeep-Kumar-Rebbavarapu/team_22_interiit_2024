from rest_framework import generics
from .serializers import MatchSerializer, ChatSerializer, MessageSerializer
from .models import MatchInfo, Chat, Message, Player
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
import pandas as pd
from datetime import datetime
import cricketstats as cks
from django.http import JsonResponse
from django.conf import settings
import os
from pathlib import Path
from django.db.models import Q
import numpy as np

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


class GetPlayerReport(APIView):
    def get(self, request):
        try:
            # Get database path using BASE_DIR
            database_path = os.path.join(settings.BASE_DIR, 'all_json.zip')

            # Ensure database file exists
            if not os.path.exists(database_path):
                return Response({
                    'success': False,
                    'error': 'Cricket database file not found. Please ensure the database is properly configured.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Get query parameters with defaults
            player_identifier = request.query_params.get('player_identifier')
            year = request.query_params.get('year')
            match_type = request.query_params.get('match_type')
            from_over = request.query_params.get('from_over')
            to_over = request.query_params.get('to_over')
            # Validate inputs
            if not all([player_identifier, year, match_type]):
                return Response({
                    'success': False,
                    'error': 'Missing required parameters. Please provide player_identifier, year, and match_type'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate overs range if provided
            betweenovers = []
            if from_over is not None or to_over is not None:
                try:
                    if from_over is not None:
                        from_over = int(from_over)
                        if from_over < 0:
                            return Response({
                                'success': False,
                                'error': 'from_over must be non-negative'
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        from_over = 1  # Default start over
                    
                    if to_over is not None:
                        to_over = int(to_over)
                        if to_over < 0:
                            return Response({
                                'success': False,
                                'error': 'to_over must be non-negative'
                            }, status=status.HTTP_400_BAD_REQUEST)
                    
                    if from_over is not None and to_over is not None and from_over > to_over:
                        return Response({
                            'success': False,
                            'error': 'from_over must be less than or equal to to_over'
                        }, status=status.HTTP_400_BAD_REQUEST)
                        
                    # Create list of overs for betweenovers parameter
                    if to_over is not None:
                        betweenovers = list(range(from_over, to_over + 1))
                    else:
                        betweenovers = [from_over]  # If only from_over is specified
                        
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'Invalid over format. Must be a whole number'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetch player name from database
            try:
                player = Player.objects.filter(identifier=player_identifier).first()
                if not player:
                    return Response({
                        'success': False,
                        'error': 'Player not found with the given identifier'
                    }, status=status.HTTP_404_NOT_FOUND)
                player_name = player.name
            except Exception as db_error:
                return Response({
                    'success': False,
                    'error': f'Database error while fetching player: {str(db_error)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Validate year
            try:
                year = int(year)
                current_year = datetime.now().year
                if year < 1900 or year > current_year:
                    return Response({
                        'success': False,
                        'error': f'Year must be between 1900 and {current_year}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'Invalid year format'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate match type
            valid_match_types = ["Test", "MDM", "ODI", "ODM", "T20", "IT20"]
            if match_type not in valid_match_types:
                return Response({
                    'success': False,
                    'error': f'Invalid match type. Must be one of: {", ".join(valid_match_types)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Initialize cricket stats search with the fetched player name
            search = cks.cricketstats.search(players=[player_name])

            # Set date range for the entire year
            from_date = (year, 1, 1)
            to_date = (year, 12, 31)

            # Perform the search with betweenovers parameter
            search.stats(
                database=database_path,
                from_date=from_date,
                to_date=to_date,
                matchtype=[match_type],
                betweenovers=betweenovers  # Using cricketstats' native overs filter
            )

            # Check if data exists
            if search.result.empty:
                return Response({
                    'success': True,
                    'message': 'No data found for the specified criteria',
                    'data': None
                }, status=status.HTTP_200_OK)

            # Process the DataFrame
            stats_data = search.result.to_dict('records')

            # Clean up the data (handle NaN, inf values and convert numpy types)
            def clean_data(item):
                cleaned = {}
                for k, v in item.items():
                    if pd.isna(v) or (isinstance(v, float) and (np.isinf(v) or np.isneginf(v))):
                        cleaned[k] = None
                    elif isinstance(v, (np.int64, np.int32)):
                        cleaned[k] = int(v)
                    elif isinstance(v, np.float64):
                        cleaned[k] = float(v) if not np.isinf(v) else None
                    elif isinstance(v, (float, int)):
                        cleaned[k] = float(v) if isinstance(v, float) else v
                    else:
                        cleaned[k] = str(v)
                return cleaned

            cleaned_stats = [clean_data(item) for item in stats_data]

            # Prepare response
            response_data = {
                'success': True,
                'data': {
                    'player_details': {
                        'identifier': player_identifier,
                        'name': player_name,
                        'year': year,
                        'match_type': match_type,
                        'overs_range': {
                            'from': from_over if from_over is not None else 1,
                            'to': to_over
                        } if betweenovers else None
                    },
                    'statistics': cleaned_stats,
                    'summary': {
                        'total_matches': len(cleaned_stats),
                        'date_range': {
                            'from': f"{from_date[0]}-{from_date[1]}-{from_date[2]}",
                            'to': f"{to_date[0]}-{to_date[1]}-{to_date[2]}"
                        }
                    }
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'error': f'An unexpected error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


