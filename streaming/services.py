"""
StreameX API Client Service
Handles all API requests to the StreameX Go backend
"""

import requests
from decouple import config
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class StreameXAPIClient:
    """Client for consuming StreameX API"""
    
    def __init__(self):
        self.base_url = config('STREAMEX_API_BASE_URL', default='http://localhost:5000/api')
        self.timeout = config('API_TIMEOUT', default=30, cast=int)
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to API
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            
        Returns:
            JSON response as dict
            
        Raises:
            requests.RequestException: On network errors
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            logger.info(f"API Request: {url} with params: {params}")
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"API Response: Success ({response.status_code})")
            return data
            
        except requests.Timeout:
            logger.error(f"API Timeout: {url}")
            return {"error": "The request took too long to complete. Please try again."}
            
        except requests.RequestException as e:
            logger.error(f"API Error: {url} - {str(e)}")
            return {"error": "Unable to connect to streaming service. Please try again later."}
            
        except ValueError as e:
            logger.error(f"JSON Parse Error: {str(e)}")
            return {"error": "Unable to process server response. Please try again later."}
    
    # ========================================
    # Search Endpoint
    # ========================================
    
    def search(self, query: str, page: int = 1) -> List[Dict]:
        """
        Search for content across all categories
        
        Args:
            query: Search keyword
            page: Page number (default: 1)
            
        Returns:
            List of search results
            
        Example:
            >>> client = StreameXAPIClient()
            >>> results = client.search("naruto", page=1)
            >>> print(results[0]['title'])
            'Naruto'
        """
        if not query or not query.strip():
            return []
            
        endpoint = "search"
        params = {
            "query": query.strip(),
            "page": page
        }
        
        response = self._make_request(endpoint, params)
        
        # Handle error response
        if isinstance(response, dict) and "error" in response:
            logger.error(f"Search error: {response['error']}")
            return []
            
        return response if isinstance(response, list) else []
    
    # ========================================
    # List Endpoints
    # ========================================
    
    def list_movies(self, page: int = 1) -> List[Dict]:
        """
        Get list of popular movies
        
        Args:
            page: Page number (default: 1)
            
        Returns:
            List of movies (20 per page)
        """
        endpoint = f"list/movie"
        params = {"page": page}
        
        response = self._make_request(endpoint, params)
        return response if isinstance(response, list) else []
    
    def list_tv_shows(self, page: int = 1) -> List[Dict]:
        """
        Get list of popular TV shows
        
        Args:
            page: Page number (default: 1)
            
        Returns:
            List of TV shows (20 per page)
        """
        endpoint = f"list/tv"
        params = {"page": page}
        
        response = self._make_request(endpoint, params)
        return response if isinstance(response, list) else []
    
    def list_anime(self, status: str = "most-popular", page: int = 1) -> List[Dict]:
        """
        Get list of anime
        
        Args:
            status: Filter status (default: "most-popular")
                   Options: most-popular, top-airing, trending, 
                           recently-added, recently-updated
            page: Page number (default: 1)
            
        Returns:
            List of anime (40 per page)
        """
        endpoint = f"list/anime"
        params = {
            "status": status,
            "page": page
        }
        
        response = self._make_request(endpoint, params)
        return response if isinstance(response, list) else []
    
    # ========================================
    # Detail Endpoints
    # ========================================
    
    def get_movie_detail(self, movie_id: str) -> Dict:
        """
        Get detailed information about a movie
        
        Args:
            movie_id: TMDB movie ID
            
        Returns:
            Movie details with streaming sources
            
        Example:
            >>> client = StreameXAPIClient()
            >>> movie = client.get_movie_detail("1265609")
            >>> print(movie['title'])
            'War Machine'
            >>> print(len(movie['episodes'][0]['sources']))
            12
        """
        endpoint = f"movie/{movie_id}"
        return self._make_request(endpoint)
    
    def get_tv_detail(self, tv_id: str, season: int = 1, episode: int = 1, providers: str = "all") -> Dict:
        """
        Get detailed information about a TV show with episode streaming
        
        Args:
            tv_id: TMDB TV show ID
            season: Season number (default: 1)
            episode: Episode number (default: 1)
            providers: Comma-separated provider names or "all" (default: "all")
            
        Returns:
            TV show details with episodes and streaming sources
            
        Example:
            >>> client = StreameXAPIClient()
            >>> tv = client.get_tv_detail("1396", season=1, episode=1)
            >>> print(tv['title'])
            'Breaking Bad'
            >>> print(tv['currentEpisode']['title'])
            'Pilot'
        """
        endpoint = f"detail/tv/{tv_id}"
        params = {
            "season": season,
            "episode": episode,
            "providers": providers
        }
        return self._make_request(endpoint, params)
    
    def get_anime_detail(self, anime_id: str, episode: int = None, providers: str = "all") -> Dict:
        """
        Get detailed information about an anime with optional episode streaming
        
        Args:
            anime_id: Anime slug (e.g., "one-piece-100")
            episode: Episode number (optional, for streaming sources)
            providers: Comma-separated provider names or "all" (default: "all")
            
        Returns:
            Anime details with episodes and streaming sources
            
        Example:
            >>> client = StreameXAPIClient()
            >>> anime = client.get_anime_detail("one-piece-100", episode=1)
            >>> print(anime['title'])
            'One Piece'
            >>> print(anime['episodes'][0]['title'])
            "I'm Luffy! The Man Who's Gonna Be King of the Pirates!"
        """
        endpoint = f"detail/anime/{anime_id}"
        params = {}
        
        if episode is not None:
            params["ep"] = episode
            params["providers"] = providers
        
        return self._make_request(endpoint, params)
    
    # ========================================
    # Provider Health Check
    # ========================================
    
    def get_provider_health(self) -> List[Dict]:
        """
        Check health status of all streaming providers
        
        Returns:
            List of provider health statuses
            
        Example:
            >>> client = StreameXAPIClient()
            >>> providers = client.get_provider_health()
            >>> for p in providers:
            ...     if p['status'] == 'up':
            ...         print(f"{p['name']}: {p['response_time']}ms")
        """
        endpoint = "providers/health"
        response = self._make_request(endpoint)
        return response if isinstance(response, list) else []
    
    # ========================================
    # Helper Methods
    # ========================================
    
    def get_content_detail(self, content_type: str, content_id: str, **kwargs) -> Dict:
        """
        Generic method to get content detail based on type
        
        Args:
            content_type: "movie", "tv", or "anime"
            content_id: Content ID
            **kwargs: Additional parameters (e.g., season for TV)
            
        Returns:
            Content details
        """
        if content_type == "movie":
            return self.get_movie_detail(content_id)
        elif content_type == "tv":
            season = kwargs.get('season', 1)
            return self.get_tv_detail(content_id, season)
        elif content_type == "anime":
            return self.get_anime_detail(content_id)
        else:
            logger.error(f"Invalid content type requested: {content_type}")
            return {"error": "Content type not supported."}
    
    def is_api_available(self) -> bool:
        """
        Check if API is available
        
        Returns:
            True if API is reachable, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/providers/health",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"API availability check failed: {str(e)}")
            return False


# Singleton instance
_client = None

def get_api_client() -> StreameXAPIClient:
    """
    Get singleton instance of API client
    
    Returns:
        StreameXAPIClient instance
    """
    global _client
    if _client is None:
        _client = StreameXAPIClient()
    return _client
