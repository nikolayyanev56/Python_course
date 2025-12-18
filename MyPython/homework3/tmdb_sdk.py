from client import TMDbClient
from exceptions import *
from models import *
from TmbdClient import *
import requests

def main():
    TMDbClient("some_key")

    url = "https://api.themoviedb.org/3/authentication"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    print(response.text)


if __name__ == "__main__":
    main()