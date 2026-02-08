import os
from MyPython.homework3.subfolder.main import TMDbClient, Genre

# Задайте ключа си тук или в env variable
api_key = os.getenv("TMDB_API_KEY", "your_key_here")

try:
    client = TMDbClient(api_key=api_key)

    print("--- Popular Movies (Limit 5) ---")
    movies = client.discover_movies(limit=5)
    for m in movies:
        print(f"{m.title} ({m.release_date})")

    print("\n--- Genre Logic Test ---")
    # Примерни ID-та (Action=28, Comedy=35)
    action = Genre(id=28, name="Action")
    comedy = Genre(id=35, name="Comedy")
    
    query = action | comedy # Action OR Comedy
    print(f"Searching for genres query: {query}")
    
    mixed_movies = client.discover_movies(genres=query, limit=3)
    for m in mixed_movies:
        print(f"{m.title} - Genres: {m.genre_ids}")

except Exception as e:
    print(f"Error: {e}")