from typing import Union
from dataclasses import dataclass

@dataclass
class Movie:
    """Stores all related information to a movie"""

    id: int
    title: str
    vote_average: float = 0.0
    original_title: str | None = None
    overview: str | None = None
    release_date: str | None = None
    poster_path: str | None = None
    backdrop_path: str | None = None
    genre_ids: list[int] | None = None
    popularity: float | None = None
    vote_count: int | None = None
    adult: bool | None = None
    original_language: str | None = None
    video: bool | None = None


@dataclass
class Series():
    """Stores all related information to Series"""

    id: int
    name: str
    vote_average: float = 0.0
    original_title: str | None = None
    overview: str | None = None
    release_date: str | None = None
    poster_path: str | None = None
    backdrop_path: str | None = None
    genre_ids: list[int] | None = None
    popularity: float | None = None
    vote_count: int | None = None
    adult: bool | None = None
    original_language: str | None = None
    video: bool | None = None


@dataclass
class Genre():
    """Stores all related information to a Genre"""

    id: int
    name: str

    def __str__(self):
        return str(self.id)
        

    def __or__(self, other: Union["Genre", "GenreQuery"]) -> "GenreQuery":

        if isinstance(other, Genre):
            return GenreQuery(f"{self.id}|{other.id}")
            
        elif isinstance(other, GenreQuery):
            return GenreQuery(f"{self.id}|{other.query_str}")


    def __and__(self, other: Union["Genre", "GenreQuery"]) -> "GenreQuery":

        if isinstance(other, Genre):
            return GenreQuery(f"{self.id},{other.id}")
            
        elif isinstance(other, GenreQuery):
            return GenreQuery(f"{self.id},{other.query_str}")


@dataclass
class GenreQuery():
    """Helper class to aid in queries to the TMDB API"""


    query_str: str

    def __str__(self):
        return self.query_str
        

    def __or__(self, other: Union["Genre", "GenreQuery"]) -> "GenreQuery":

        if isinstance(other, Genre):
            return GenreQuery(f"{self.query_str} | {other.id}")
            
        elif isinstance(other, GenreQuery):
            return GenreQuery(f"{self.query_str} | {other.query_str}")


    def __and__(self, other: Union["Genre", "GenreQuery"]) -> "GenreQuery":
            
        if isinstance(other, Genre):
            return GenreQuery(f"{self.query_str},{other.id}")
            
        if isinstance(other, GenreQuery):
            return GenreQuery(f"{self.query_str},{other.query_str}")