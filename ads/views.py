from django.shortcuts import render


def home(request):
    """Homepage with featured content"""
    context = {
        'page_type': 'home'
    }
    return render(request, 'streaming/home.html', context)


def player(request):
    """Video player page"""
    context = {
        'page_type': 'player'
    }
    return render(request, 'streaming/player.html', context)


def anime(request):
    """Anime listing page"""
    context = {
        'page_type': 'anime'
    }
    return render(request, 'streaming/home.html', context)


def movie(request):
    """Movie listing page"""
    context = {
        'page_type': 'movie'
    }
    return render(request, 'streaming/home.html', context)


def series(request):
    """Series listing page"""
    context = {
        'page_type': 'series'
    }
    return render(request, 'streaming/home.html', context)
