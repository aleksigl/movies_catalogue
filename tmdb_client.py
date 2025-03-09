import requests, random


def get_popular_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYmI1OTEzYmI5OWE0MzA3YjMzMzM1ODhhNTUwZDJhMCIsIm5iZiI6MTc0MTM2NjM2Mi43NzUsInN1YiI6IjY3Y2IyNDVhZGJhMTQ5MTYwNjJiNmMwZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-CIgdFVi3K9-UrzKNpM8pq7IEDoaRyNB7kGfl_Y3LH8"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    results = requests.get(url, headers=headers)
    if results.status_code == 200:
        return results.json().get("results", [])
    else:
        return []

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_movie_info():
    info = get_popular_movies()
    movie_dict = {
        movie["title"] : get_poster_url(movie["poster_path"])
        for movie in info if movie.get("poster_path")
    }
    return movie_dict

def get_movies():
    data = random.sample(get_popular_movies(), 12)
    return data
