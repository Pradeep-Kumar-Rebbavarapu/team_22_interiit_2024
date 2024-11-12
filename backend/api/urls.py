from django.urls import path,include
from .views import MatchList
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('matches/', MatchList.as_view(), name='match-list')
]
