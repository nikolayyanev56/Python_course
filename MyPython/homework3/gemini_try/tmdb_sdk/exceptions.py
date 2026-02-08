class TMDBException(Exception):
    """Base class for all TMDB SDK exceptions."""
    pass

class TMDBAuthenticationError(TMDBException):
    """Raised when authentication fails (HTTP 401)."""
    pass

class TMDBNotFoundError(TMDBException):
    """Raised when a resource is not found (HTTP 404)."""
    pass

class TMDBRateLimitError(TMDBException):
    """Raised when rate limit is exceeded (HTTP 429)."""
    pass

class TMDBServerError(TMDBException):
    """Raised when TMDB server encounters an error (HTTP 5xx)."""
    pass