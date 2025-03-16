import requests
import random
from datetime import datetime

api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYmI1OTEzYmI5OWE0MzA3YjMzMzM1ODhhNTUwZDJhMCIsIm5iZiI6MTc0MTM2NjM2Mi43NzUsInN1YiI6IjY3Y2IyNDVhZGJhMTQ5MTYwNjJiNmMwZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-CIgdFVi3K9-UrzKNpM8pq7IEDoaRyNB7kGfl_Y3LH8"


def get_movies_list(list_name="popular"):
    url = f"https://api.themoviedb.org/3/movie/{list_name}"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    results = requests.get(url, headers=headers)
    results.raise_for_status()
    if results.status_code == 200:
        return results.json().get("results", [])
    else:
        return []


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
    data = random.sample(get_movies_list(list_name), 12)
    return data


def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        movie_data = response.json()
        if 'release_date' in movie_data:
            movie_data['release_date'] = datetime.strptime(movie_data['release_date'], "%Y-%m-%d").year
        return movie_data
    else:
        print(f"Error fetching movie data: {response.status_code}")
        return {}


def get_large_poster(backdrop_path, size="w780"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{backdrop_path}"


def get_single_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        cast_data = response.json().get("cast", [])
        return cast_data[:12]
    else:
        print("Error fetching cast:", response.status_code, response.text)
        return []


def get_movie_images(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def search(search_query):
    base_url = "https://api.themoviedb.org/3/"
    headers = {
       "Authorization": f"Bearer {api_token}"
    }
    endpoint = f"{base_url}search/movie?query={search_query}"

    response = requests.get(endpoint, headers=headers)
    response = response.json()
    return response['results']
