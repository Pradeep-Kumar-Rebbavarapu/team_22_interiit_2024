from django.urls import path
from .views import MatchList, ChatList, ChatDetail,GetPlayerReport


urlpatterns = [
    path('matches/', MatchList.as_view(), name='match-list'),
    path('get-player-report/',GetPlayerReport.as_view()),
]
