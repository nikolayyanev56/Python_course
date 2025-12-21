class TMDBException(Exception):
    """Base class for all errors in the TMDB_SDK"""
    pass

class TMDBAuthenticationError(TMDBException):
    """For errors in authenticating with TMDB"""
    pass

class TMDBNotFoundError(TMDBException):
    """For resources not found TMDB"""
    pass

class TMDBRateLimitError(TMDBException):
    """For exeeding the rate limit"""
    pass

class TMDBServerError(TMDBException):
    """For serverside errors with TMDB"""
    pass