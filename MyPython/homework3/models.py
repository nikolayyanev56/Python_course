class Movie():
      def __init__(
        self,
        id: int,
        title: str,
        vote_average: float = 0.0,
        original_title: str | None = None,
        overview: str | None = None,
        release_date: str | None = None,
        poster_path: str | None = None,
        backdrop_path: str | None = None,
        genre_ids: list[int] | None = None,
        popularity: float | None = None,
        vote_count: int | None = None,
        adult: bool | None = None,
        original_language: str | None = None,
        video: bool | None = None
    ):
        
        self.id = id
        self.title = title
        self.vote_average = vote_average
        self.original_title = original_title
        self.overview = overview
        self.release_date = release_date
        self.poster_path = poster_path
        self.backdrop_path = backdrop_path
        self.genre_ids = genre_ids
        self.popularity = popularity
        self.vote_count = vote_count
        self.adult = adult
        self.original_language = original_language
        self.video = video


class Series():

    def __init__(
        self,
        id: int,
        title: str,
        vote_average: float = 0.0,
        original_title: str | None = None,
        overview: str | None = None,
        release_date: str | None = None,
        poster_path: str | None = None,
        backdrop_path: str | None = None,
        genre_ids: list[int] | None = None,
        popularity: float | None = None,
        vote_count: int | None = None,
        adult: bool | None = None,
        original_language: str | None = None,
        video: bool | None = None,
    ):
        
        self.id = id
        self.title = title
        self.vote_average = vote_average
        self.original_title = original_title
        self.overview = overview
        self.release_date = release_date
        self.poster_path = poster_path
        self.backdrop_path = backdrop_path
        self.genre_ids = genre_ids
        self.popularity = popularity
        self.vote_count = vote_count
        self.adult = adult
        self.original_language = original_language
        self.video = video


class Genre():
    def __init__(
        self,
        id: int,
        name: str,
        ):
            self.id = id
            self.name = name


class GenreQuery():
    def __init__(self):
        pass