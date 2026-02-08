from dataclasses import dataclass, field
from typing import Optional, Union

@dataclass
class Movie:
    id: int
    title: str
    vote_average: float = 0.0
    original_title: Optional[str] = None
    overview: Optional[str] = None
    release_date: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    genre_ids: Optional[list[int]] = None
    popularity: Optional[float] = None
    vote_count: Optional[int] = None
    adult: Optional[bool] = None
    original_language: Optional[str] = None
    video: Optional[bool] = None

@dataclass
class Series:
    id: int
    name: str
    vote_average: float = 0.0
    original_name: Optional[str] = None
    overview: Optional[str] = None
    first_air_date: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    genre_ids: Optional[list[int]] = None
    popularity: Optional[float] = None
    vote_count: Optional[int] = None
    original_language: Optional[str] = None

class GenreQuery:
    """Helper class to construct complex genre queries with AND/OR logic."""
    def __init__(self, query_str: str):
        self.query_str = query_str

    def __str__(self) -> str:
        return self.query_str

    def __and__(self, other: Union["Genre", "GenreQuery"]) -> "GenreQuery":
        if isinstance(other, Genre):
            return GenreQuery(f"{self.query_str},{other.id}")
        elif isinstance(other, GenreQuery):
            return GenreQuery(f"{self.query_str},{other.query_str}")
        return NotImplemented

    def __or__(self, other: Union["Genre", "GenreQuery"]) -> "GenreQuery":
        if isinstance(other, Genre):
            return GenreQuery(f"{self.query_str}|{other.id}")
        elif isinstance(other, GenreQuery):
            return GenreQuery(f"{self.query_str}|{other.query_str}")
        return NotImplemented

@dataclass
class Genre:
    id: int
    name: str

    def __str__(self) -> str:
        return str(self.id)

    def __and__(self, other: Union["Genre", GenreQuery]) -> GenreQuery:
        if isinstance(other, Genre):
            return GenreQuery(f"{self.id},{other.id}")
        elif isinstance(other, GenreQuery):
            return GenreQuery(f"{self.id},{other.query_str}")
        return NotImplemented

    def __or__(self, other: Union["Genre", GenreQuery]) -> GenreQuery:
        if isinstance(other, Genre):
            return GenreQuery(f"{self.id}|{other.id}")
        elif isinstance(other, GenreQuery):
            return GenreQuery(f"{self.id}|{other.query_str}")
        return NotImplemented