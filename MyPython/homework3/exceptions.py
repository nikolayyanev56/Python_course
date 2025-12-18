class TMDBExcetion(Exception):
    pass

class TMDBAuthenticationError(TMDBExcetion):
    pass

class TMDBNotFoundError(TMDBExcetion):
    pass

class TMDBRateLimitError(TMDBExcetion):
    pass

class TMDBServerError(TMDBExcetion):
    pass