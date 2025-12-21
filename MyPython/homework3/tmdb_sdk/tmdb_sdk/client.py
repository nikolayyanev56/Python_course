import requests
from typing import Any, TypeVar
from .models import Series, Movie, Genre, GenreQuery
from .exceptions import TMDBAuthenticationError, TMDBException, TMDBNotFoundError, TMDBRateLimitError, TMDBServerError

T = TypeVar("T")

class TMDBClient():
    """Loads information about the client like the API key"""

    #/3 for version 3
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(
        self,
        api_key: str | None = None
    ):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.params = {"api_key": self.api_key}

    
    def _get_response(self, response: requests.Response) -> None:
        """Checks server response code and raises apropriate errors"""

        #pass if there are no errors
        if response.status_code == 200:
            return
        

        if response.status_code == 401:
            raise TMDBAuthenticationError(f"Error 401 Unauthorized: {response.text}")
        
        elif response.status_code == 404:
            raise TMDBNotFoundError(f"Error 404 Not Found: {response.text}")
        
        elif response.status_code == 429:
            raise TMDBRateLimitError(f"Error 429 Rate Limit Exceeded: {response.text}")
        
        elif 500 <= response.status_code < 600:
            raise TMDBServerError(f"Server Error {response.status_code}: {response.text}")
        
        else:
            raise TMDBException(f"Other Error {response.status_code}: {response.text}")


    def _get_paginated(
        self,
        endpoint: str,
        model_class: type[T],
        params: dict,
        limit: int,
        results_key: str = "results"
    ) -> list[T]:
        """Helper function to deal with the limit parameter and the pagination"""
        
        if limit < 1:
            raise ValueError("Limit must a number above 0")

        results: list[T] = []
        current_page = 1
        
        while len(results) < limit:

            params["page"] = current_page
            
            try:
                response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
                self._get_response(response)
                data = response.json()

            except requests.RequestException as ex:
                raise TMDBException(f"Connection Error: {ex}")

            items = data.get(results_key, [])

            if not items:
                break

            for item in items:
                results.append(self._map_to_model(model_class, item))
                if len(results) >= limit:
                    break
            
            total_pages = data.get("total_pages", 0)
            if current_page >= total_pages:
                break
                
            current_page += 1

        return results


    def _valid_genre_params(
        self,
        genres: Genre | GenreQuery | None = None
    ) -> None:
        """Checks if param genre is actually the right type"""

        if genres is not None and not isinstance(genres, (Genre, GenreQuery)):
            raise ValueError(f"Genre must of type Genre, GenreQuery or None")
        
    
    def _map_to_model(self, model_class: type[T], data: dict) -> T:
        """Helper to collect only the necessary data from the response JSON"""

        field_names = {f.name for f in model_class.__dataclass_fields__.values()}

        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return model_class(**filtered_data)


    def discover_movies(
        self,
        language: str | None = None,
        region: str | None = None,
        sort_by: str | None = None,
        year: int | None = None,
        genres: Genre | GenreQuery | None = None,
        limit: int = 10,
    ) -> list[Movie]:

        self._valid_genre_params(genres)

        params: dict[str, Any] ={}
        if language: params["language"] = language
        if region: params["region"] = region
        if sort_by: params["sort_by"] = sort_by
        if year: params["year"] = year
        if genres: params["with_genres"] = str(genres)

        return self._get_paginated("/discover/movie", Movie, params, limit)


    def discover_series(
        self,
        language: str | None = None,
        sort_by: str | None = None,
        genres: Genre | GenreQuery | None = None,
        limit: int = 10,
    ) -> list[Series]:
        
        self._valid_genre_params(genres)

        params: dict[str, Any] = {}
        if language: params["language"] = language
        if sort_by: params["sort_by"] = sort_by
        if genres: params["with_genres"] = str(genres)

        return self._get_paginated("/discover/tv", Series, params, limit)


    def get_movie_genres(
        self,
        language: str | None = None,
    ) -> list[Genre]:

        params: dict[str, Any] = {}
        if language: params["language"] = language
        
        response = self.session.get(f"{self.BASE_URL}/genre/movie/list", params=params)
        self._get_response(response)
        data = response.json()

        return [self._map_to_model(Genre, item) for item in data.get("genres", [])]


    def get_series_genres(
        self,
        language: str | None = None,
    ) -> list[Genre]:
        
        params: dict[str, Any] = {}
        if language: params["language"] = language
        
        response = self.session.get(f"{self.BASE_URL}/genre/tv/list", params=params)
        self._get_response(response)
        data = response.json()

        return [self._map_to_model(Genre, item) for item in data.get("genres", [])]


    def search_movies(
        self,
        query: str,
        language: str | None = None,
        year: int | None = None,
        limit: int = 10,
    ) -> list[Movie]:
       
        params: dict[str, Any] = {"query": query}
        if language: params["language"] = language
        if year: params["primary_release_year"] = year

        return self._get_paginated("/search/movie", Movie, params, limit)

    def search_series(
        self,
        query: str,
        language: str | None = None,
        limit: int = 10,
    ) -> list[Series]:
        
        params: dict[str, Any] = {"query": query}
        if language: params["language"] = language

        return self._get_paginated("/search/tv", Series, params, limit)