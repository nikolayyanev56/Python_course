import requests
from typing import Optional, Type, TypeVar, List, Any, Union
from tmdb_sdk.models import Movie, Series, Genre, GenreQuery
from tmdb_sdk.exceptions import (
    TMDBAuthenticationError,
    TMDBNotFoundError,
    TMDBRateLimitError,
    TMDBServerError,
    TMDBException
)

T = TypeVar("T")

class TMDbClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
        
        self.api_key = api_key
        self.session = requests.Session()
        # Authentication can be passed via query param or Bearer token.
        # Standard generic approach for TMDb is query param 'api_key' 
        # or Authorization header. We will use query params for simplicity 
        # in each request or inject it into params.
        self.session.params = {"api_key": self.api_key}

    def _check_response(self, response: requests.Response) -> None:
        """Parses the status code and raises appropriate custom exceptions."""
        if response.status_code == 200:
            return
        
        if response.status_code == 401:
            raise TMDBAuthenticationError(f"401 Unauthorized: {response.text}")
        elif response.status_code == 404:
            raise TMDBNotFoundError(f"404 Not Found: {response.text}")
        elif response.status_code == 429:
            raise TMDBRateLimitError(f"429 Rate Limit Exceeded: {response.text}")
        elif 500 <= response.status_code < 600:
            raise TMDBServerError(f"Server Error {response.status_code}: {response.text}")
        else:
            # Fallback for other errors (e.g., 400 Bad Request)
            raise TMDBException(f"Error {response.status_code}: {response.text}")

    def _map_to_model(self, model_class: Type[T], data: dict) -> T:
        """
        Helper to safely instantiate a dataclass from a dict, 
        ignoring extra keys in the JSON response.
        """
        # Get the field names of the dataclass
        field_names = {f.name for f in model_class.__dataclass_fields__.values()} # type: ignore
        # Filter the data dictionary to only include valid fields
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return model_class(**filtered_data)

    def _fetch_paginated(
        self, 
        endpoint: str, 
        model_class: Type[T], 
        params: dict, 
        limit: int,
        results_key: str = "results"
    ) -> List[T]:
        """
        Handles pagination logic manually to satisfy the 'limit' requirement.
        """
        if limit < 1:
            raise ValueError("Limit must be a positive integer")

        results: List[T] = []
        current_page = 1
        
        # Keep fetching while we don't have enough results
        while len(results) < limit:
            params["page"] = current_page
            
            try:
                response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
                self._check_response(response)
                data = response.json()
            except requests.RequestException as e:
                # Catch connection errors not handled by status check
                raise TMDBException(f"Connection error: {e}")

            items = data.get(results_key, [])
            if not items:
                break # No more results available

            for item in items:
                results.append(self._map_to_model(model_class, item))
                if len(results) >= limit:
                    break
            
            total_pages = data.get("total_pages", 0)
            if current_page >= total_pages:
                break
                
            current_page += 1

        return results[:limit]

    def _validate_genre_param(self, genres: Optional[Union[Genre, GenreQuery]]) -> None:
        if genres is not None and not isinstance(genres, (Genre, GenreQuery)):
            raise TypeError("Genres must be of type Genre, GenreQuery, or None")

    def discover_movies(
        self,
        language: Optional[str] = None,
        region: Optional[str] = None,
        sort_by: Optional[str] = None,
        year: Optional[int] = None,
        genres: Optional[Union[Genre, GenreQuery]] = None,
        limit: int = 10,
    ) -> List[Movie]:
        
        self._validate_genre_param(genres)
        
        params: dict[str, Any] = {}
        if language: params["language"] = language
        if region: params["region"] = region
        if sort_by: params["sort_by"] = sort_by
        if year: params["primary_release_year"] = year
        if genres: params["with_genres"] = str(genres)

        return self._fetch_paginated("/discover/movie", Movie, params, limit)

    def discover_series(
        self,
        language: Optional[str] = None,
        sort_by: Optional[str] = None,
        genres: Optional[Union[Genre, GenreQuery]] = None,
        limit: int = 10,
    ) -> List[Series]:
        
        self._validate_genre_param(genres)

        params: dict[str, Any] = {}
        if language: params["language"] = language
        if sort_by: params["sort_by"] = sort_by
        if genres: params["with_genres"] = str(genres)

        return self._fetch_paginated("/discover/tv", Series, params, limit)

    def get_movie_genres(self, language: Optional[str] = None) -> List[Genre]:
        params: dict[str, Any] = {}
        if language: params["language"] = language
        
        response = self.session.get(f"{self.BASE_URL}/genre/movie/list", params=params)
        self._check_response(response)
        
        data = response.json()
        return [self._map_to_model(Genre, item) for item in data.get("genres", [])]

    def get_series_genres(self, language: Optional[str] = None) -> List[Genre]:
        params: dict[str, Any] = {}
        if language: params["language"] = language
        
        response = self.session.get(f"{self.BASE_URL}/genre/tv/list", params=params)
        self._check_response(response)
        
        data = response.json()
        return [self._map_to_model(Genre, item) for item in data.get("genres", [])]

    def search_movies(
        self,
        query: str,
        language: Optional[str] = None,
        year: Optional[int] = None,
        limit: int = 10,
    ) -> List[Movie]:
        
        params: dict[str, Any] = {"query": query}
        if language: params["language"] = language
        if year: params["primary_release_year"] = year

        return self._fetch_paginated("/search/movie", Movie, params, limit)

    def search_series(
        self,
        query: str,
        language: Optional[str] = None,
        limit: int = 10,
    ) -> List[Series]:
        
        params: dict[str, Any] = {"query": query}
        if language: params["language"] = language

        return self._fetch_paginated("/search/tv", Series, params, limit)