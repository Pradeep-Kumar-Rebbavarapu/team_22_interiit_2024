from django.urls import path
from .views import MatchList, ChatList, ChatDetail,GetPlayerReport,ChatList


urlpatterns = [
    path('matches/', MatchList.as_view(), name='match-list'),
    path('get-player-report/',GetPlayerReport.as_view()),
    path('get-match-related-chats/',ChatList.as_view()),
]
