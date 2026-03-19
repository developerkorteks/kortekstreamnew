"""
Streaming Views - Consume StreameX API
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from .services import get_api_client
import logging

logger = logging.getLogger(__name__)


def home(request):
    """Homepage - Show popular movies"""
    api = get_api_client()
    page = request.GET.get('page', 1)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    # Get popular movies
    movies = api.list_movies(page=page)
    
    # Use first item as hero content
    hero_content = movies[0] if movies else None
    
    context = {
        'page_type': 'home',
        'movies': movies,
        'hero_content': hero_content,
        'current_page': page,
        'title': 'Popular Movies',
    }
    
    return render(request, 'streaming/home.html', context)


def search(request):
    """Search for content"""
    query = request.GET.get('q', '').strip()
    page = request.GET.get('page', 1)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    results = []
    if query:
        api = get_api_client()
        results = api.search(query, page=page)
    
    context = {
        'page_type': 'search',
        'query': query,
        'results': results,
        'current_page': page,
        'title': f'Search: {query}' if query else 'Search',
    }
    
    return render(request, 'streaming/search.html', context)


def movie_list(request):
    """List popular movies"""
    api = get_api_client()
    page = request.GET.get('page', 1)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    movies = api.list_movies(page=page)
    
    # Use first item as hero content
    hero_content = movies[0] if movies else None
    
    context = {
        'page_type': 'movie',
        'movies': movies,
        'hero_content': hero_content,
        'current_page': page,
        'title': 'Popular Movies',
    }
    
    return render(request, 'streaming/home.html', context)


def tv_list(request):
    """List popular TV shows"""
    api = get_api_client()
    page = request.GET.get('page', 1)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    tv_shows = api.list_tv_shows(page=page)
    
    # Use first item as hero content
    hero_content = tv_shows[0] if tv_shows else None
    
    context = {
        'page_type': 'series',
        'movies': tv_shows,  # Using 'movies' for template compatibility
        'hero_content': hero_content,
        'current_page': page,
        'title': 'Popular TV Shows',
    }
    
    return render(request, 'streaming/home.html', context)


def anime_list(request):
    """List popular anime"""
    api = get_api_client()
    page = request.GET.get('page', 1)
    status = request.GET.get('status', 'most-popular')
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    anime = api.list_anime(status=status, page=page)
    
    # Use first item as hero content
    hero_content = anime[0] if anime else None
    
    context = {
        'page_type': 'anime',
        'movies': anime,  # Using 'movies' for template compatibility
        'hero_content': hero_content,
        'current_page': page,
        'status': status,
        'title': f'Anime - {status.replace("-", " ").title()}',
    }
    
    return render(request, 'streaming/home.html', context)


def profile_view(request):
    """User Profile Page - Mock data for prototype"""
    mock_user = {
        'username': 'Kurosaw_Fan',
        'avatar': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&q=80&w=200',
        'banner': 'https://images.unsplash.com/photo-1614728263952-84ea256f9679?auto=format&fit=crop&q=80&w=1200',
        'stats': {
            'watching': 12,
            'to_watch': 45,
            'watched': 128,
            'collections': 8
        }
    }
    
    # Mock watchlist from API (using popular movies as example)
    api = get_api_client()
    watchlist = api.list_movies(page=1)[:6]
    
    context = {
        'page_type': 'profile',
        'user_profile': mock_user,
        'watchlist': watchlist,
        'title': 'Kurosaw Profile',
    }
    
    return render(request, 'streaming/profile.html', context)


def news_list(request):
    """News and Articles Page - Mock data for prototype"""
    mock_news = [
        {
            'id': 1,
            'title': 'Season 2 of Chainsaw Man Confirmed: Denji returns this Fall!',
            'thumbnail': 'https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?auto=format&fit=crop&q=80&w=1200',
            'timestamp': '2h ago',
            'category': 'ANIME',
            'featured': True,
            'summary': 'The highly anticipated second season of Chainsaw Man has finally been confirmed by the studio. Fans can expect Denji to return this October with even more brutal action and emotional storytelling.'
        },
        {
            'id': 2,
            'title': "War Machine: Why this movie is a game changer for Sci-Fi",
            'thumbnail': 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=800',
            'timestamp': '5h ago',
            'category': 'MOVIE',
            'featured': False,
            'summary': "Dive into the technical marvels and gritty storytelling that make 'War Machine' the must-watch film of 2026."
        },
        {
            'id': 3,
            'title': 'The Rookie Season 7: Behind the scenes of the premiere',
            'thumbnail': 'https://images.unsplash.com/photo-1585951237318-9ea5e175b891?auto=format&fit=crop&q=80&w=800',
            'timestamp': '1d ago',
            'category': 'SERIES',
            'featured': False,
            'summary': 'Exclusive photos and interviews with the cast of The Rookie as they return for their most ambitious season yet.'
        },
        {
            'id': 4,
            'title': 'Top 10 Dark Fantasy Anime You Need To Watch Right Now',
            'thumbnail': 'https://images.unsplash.com/photo-1578632738981-4330c7091f3d?auto=format&fit=crop&q=80&w=800',
            'timestamp': '2d ago',
            'category': 'COLLECTIONS',
            'featured': False,
            'summary': 'From Jujutsu Kaisen to Berserk, explore the best dark fantasy anime that will leave you at the edge of your seat.'
        },
        {
            'id': 5,
            'title': 'Exploring the World of Cyberpunk Edgerunners Lore',
            'thumbnail': 'https://images.unsplash.com/photo-1614728263952-84ea256f9679?auto=format&fit=crop&q=80&w=800',
            'timestamp': '3d ago',
            'category': 'ANIME',
            'featured': False,
            'summary': 'A deep dive into the Night City lore that wasn\'t fully explored in the series.'
        },
    ]
    
    context = {
        'page_type': 'news',
        'news': mock_news,
        'title': 'Kurosaw News',
    }
    
    return render(request, 'streaming/news.html', context)


def movie_detail(request, movie_id):
    """Movie detail and player"""
    api = get_api_client()
    movie = api.get_movie_detail(movie_id)
    
    # Check for error
    if 'error' in movie:
        logger.error(f"Movie detail error for ID {movie_id}: {movie['error']}")
        context = {
            'error_message': 'Unable to load this movie. Please try again later.',
            'title': 'Error',
        }
        return render(request, 'streaming/error.html', context)
    
    # Extract sources for unified access (from episodes[0].sources for movies)
    sources = []
    if movie.get('episodes') and len(movie['episodes']) > 0:
        sources = movie['episodes'][0].get('sources', [])
    
    context = {
        'page_type': 'player',
        'content': movie,
        'content_type': 'movie',
        'sources': sources,
        'title': movie.get('title', 'Movie'),
    }
    
    return render(request, 'streaming/player.html', context)


def tv_detail(request, tv_id):
    """TV show detail and player"""
    api = get_api_client()
    
    # Get parameters from request
    season = request.GET.get('season', 1)
    episode = request.GET.get('episode', 1)
    provider = request.GET.get('provider', 'all')
    
    # Convert to integers
    try:
        season = int(season)
        episode = int(episode)
    except ValueError:
        season = 1
        episode = 1
    
    # Get TV show with episode details and streaming sources
    tv_show = api.get_tv_detail(tv_id, season=season, episode=episode, providers=provider)
    
    # Check for error
    if 'error' in tv_show:
        logger.error(f"TV detail error for ID {tv_id}: {tv_show['error']}")
        context = {
            'error_message': 'Unable to load this TV show. Please try again later.',
            'title': 'Error',
        }
        return render(request, 'streaming/error.html', context)
    
    # Extract sources from the correct episode
    sources = []
    if tv_show.get('episodes') and len(tv_show['episodes']) > 0:
        # Find the episode that matches the requested episode number
        target_episode = None
        for ep in tv_show['episodes']:
            if ep.get('episode_number') == episode:
                target_episode = ep
                break
        
        # Fallback to the first episode if not found
        if not target_episode:
            target_episode = tv_show['episodes'][0]
            
        sources = target_episode.get('sources', [])
    
    context = {
        'page_type': 'player',
        'content': tv_show,
        'content_type': 'tv',
        'current_season': season,
        'current_episode': episode,
        'sources': sources,
        'title': tv_show.get('title', 'TV Show'),
    }
    
    return render(request, 'streaming/player.html', context)


def anime_detail(request, anime_id):
    """Anime detail and player"""
    api = get_api_client()
    
    # Get parameters from request
    episode = request.GET.get('ep')
    provider = request.GET.get('provider', 'all')
    
    # Convert episode to int if provided
    if episode:
        try:
            episode = int(episode)
        except ValueError:
            episode = None
    
    # Get anime details with optional episode streaming
    anime = api.get_anime_detail(anime_id, episode=episode, providers=provider)
    
    # Check for error
    if 'error' in anime:
        logger.error(f"Anime detail error for ID {anime_id}: {anime['error']}")
        context = {
            'error_message': 'Unable to load this anime. Please try again later.',
            'title': 'Error',
        }
        return render(request, 'streaming/error.html', context)
    
    # Extract extra info for template
    anime_info = anime.get('animeInfo', {})
    
    # Extract sources for the requested or first episode
    sources = []
    if anime.get('episodes') and len(anime['episodes']) > 0:
        # If episode number is specified, search for it in the episodes list
        if episode:
            target_episode = None
            for ep in anime['episodes']:
                # Anime often uses 'episode_no' or 'episode_number'
                ep_num = ep.get('episode_no') or ep.get('episode_number')
                if ep_num == episode:
                    target_episode = ep
                    break
            
            # If target not found, fallback to first episode
            if not target_episode:
                target_episode = anime['episodes'][0]
        else:
            # If no episode specified, default to first episode
            target_episode = anime['episodes'][0]
            
        sources = target_episode.get('sources', [])
    
    context = {
        'page_type': 'player',
        'content': anime,
        'anime_info': anime_info,
        'content_type': 'anime',
        'current_episode': episode,
        'sources': sources,
        'title': anime.get('title', 'Anime'),
    }
    
    return render(request, 'streaming/player.html', context)


def api_health(request):
    """Check API health status"""
    api = get_api_client()
    providers = api.get_provider_health()
    
    # Calculate statistics
    total = len(providers)
    up = sum(1 for p in providers if p.get('status') == 'up')
    down = sum(1 for p in providers if p.get('status') == 'down')
    unstable = sum(1 for p in providers if p.get('status') == 'unstable')
    
    stats = {
        'total': total,
        'up': up,
        'down': down,
        'unstable': unstable,
        'percentage': round((up / total * 100) if total > 0 else 0, 2)
    }
    
    return JsonResponse({
        'providers': providers,
        'stats': stats,
        'api_available': api.is_api_available()
    })


# ========================================
# Custom Error Handlers
# ========================================

def custom_404(request, exception):
    """Custom 404 error handler"""
    logger.warning(f"404 Error: {request.path}")
    return render(request, '404.html', status=404)


def custom_500(request):
    """Custom 500 error handler"""
    logger.error(f"500 Error on path: {request.path}")
    return render(request, '500.html', status=500)


def custom_403(request, exception):
    """Custom 403 error handler"""
    logger.warning(f"403 Error: {request.path}")
    return render(request, '403.html', status=403)


def custom_400(request, exception):
    """Custom 400 error handler"""
    logger.warning(f"400 Error: {request.path}")
    return render(request, '400.html', status=400)
