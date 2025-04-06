import requests
import random
from datetime import datetime

import os
api_token = os.environ.get("TMDB_API_TOKEN")


def call_tmdb_api(endpoint):
    url = f"https://api.themoviedb.org/3/{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    results = requests.get(url, headers=headers)
    results.raise_for_status()
    if results.status_code == 200:
        return results.json()
    else:
        print(f"Error fetching movie data: {results.status_code}")
        return []


def get_movies_list(list_name="popular"):
    json_response = call_tmdb_api(f"movie/{list_name}")
    results = json_response.get("results", [])
    return results


def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"


def get_movie_info():
    info = get_movies_list(list_name="popular")
    movie_dict = {
        movie["title"]: get_poster_url(movie["poster_path"])
        for movie in info if movie.get("poster_path")
    }
    return movie_dict


def get_movies(list_name="popular"):
    movie_list = get_movies_list(list_name)
    sample_size = min(12, len(movie_list))
    data = random.sample(movie_list, sample_size)
    return data


def get_single_movie(movie_id):
    movie_data = call_tmdb_api(f"movie/{movie_id}")
    if 'release_date' in movie_data:
        if isinstance(movie_data['release_date'], str):
            movie_data['release_date'] = datetime.strptime(movie_data['release_date'], "%Y-%m-%d").year
    return movie_data


def get_large_poster(backdrop_path, size="w780"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{backdrop_path}"


def get_single_movie_cast(movie_id):
    result = call_tmdb_api(f"movie/{movie_id}/credits")
    cast_data = result.get("cast", [])
    return cast_data[:12]


def get_movie_images(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def search(search_query):
    response = call_tmdb_api(f"search/movie?query={search_query}")
    return response['results']
