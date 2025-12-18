class TMDbClient():
    def __init__(
        self,
        api_key: str | None = None
        ):
        
        self.api_key = api_key