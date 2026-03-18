"""
Streaming URL Configuration
"""

from django.urls import path
from . import views

app_name = 'streaming'

urlpatterns = [
    # Home and lists
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile_view, name='profile_view'),
    
    # Category lists
    path('movies/', views.movie_list, name='movie_list'),
    path('tv/', views.tv_list, name='tv_list'),
    path('anime/', views.anime_list, name='anime_list'),
    
    # Detail pages
    path('movie/<str:movie_id>/', views.movie_detail, name='movie_detail'),
    path('tv/<str:tv_id>/', views.tv_detail, name='tv_detail'),
    path('anime/<str:anime_id>/', views.anime_detail, name='anime_detail'),
    
    # API health
    path('api/health/', views.api_health, name='api_health'),
]
