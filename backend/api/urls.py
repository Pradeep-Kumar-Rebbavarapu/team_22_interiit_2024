from django.urls import path
from .views import MatchList, ChatList, ChatDetail,GetPlayerReport,ChatList,PredictPlayers,GetAllPlayers , GetAllTeams , MatchCreateAPIView


urlpatterns = [
    path('matches/', MatchList.as_view(), name='match-list'),
    path('get-player-report/',GetPlayerReport.as_view()),
    path('get-match-related-chats/',ChatList.as_view()),
    path('predict-players/',PredictPlayers.as_view()),
    path('players/',GetAllPlayers.as_view()),
    path('teams/',GetAllTeams.as_view()),
    path('add-match/',MatchCreateAPIView.as_view()),
]
