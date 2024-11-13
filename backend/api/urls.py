from django.urls import path
from .views import MatchList, MatchDetail, ChatList, ChatDetail
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('matches/', MatchList.as_view(), name='match-list'),
    path('matches/<int:pk>/', MatchDetail.as_view(), name='match-detail'),
]
