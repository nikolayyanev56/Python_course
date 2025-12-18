from models import *

def discover_movies(
    language: str | None = None,
    region: str | None = None,
    sort_by: str | None = None,
    year: int | None = None,
    genres: Genre | GenreQuery | None = None,
    limit: int = 10,
) -> list[Movie]:
    pass


def discover_series(
    language: str | None = None,
    sort_by: str | None = None,
    genres: Genre | GenreQuery | None = None,
    limit: int = 10,
) -> list[Series]:
    pass




def get_movie_genres(
    language: str | None = None,
) -> list[Genre]:
    pass


def get_series_genres(
    language: str | None = None,
) -> list[Genre]:
    pass


def search_movies(
    query: str,
    language: str | None = None,
    year: int | None = None,
    limit: int = 10,
) -> list[Movie]:
    pass


def search_series(
    query: str,
    language: str | None = None,
    limit: int = 10,
) -> list[Series]:
    return [query, language, limit]


