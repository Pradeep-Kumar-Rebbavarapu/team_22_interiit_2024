from django.urls import path
from .views import MatchList, ChatList, ChatDetail
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('matches/', MatchList.as_view(), name='match-list')
]
