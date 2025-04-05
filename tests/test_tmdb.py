import tmdb_client
from tmdb_client import *
from unittest.mock import Mock


def test_get_single_movie(monkeypatch):
    mock_single_movie = {
        'id': 123,
        'title': "Sample Movie",
        'release_date': "2022-05-02",
        'overview': "A sample movie for testing purposes."
    }
    mock_call_tmdb_api = Mock(return_value=mock_single_movie)
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)
    movie_id = 123
    movie_data = get_single_movie(movie_id)
    assert movie_data == mock_single_movie
    mock_call_tmdb_api.assert_called_once_with(f"movie/{movie_id}")


def test_get_movie_images(monkeypatch):
    mock_images = {
        "id": 789,
        "backdrops": [
            {
                "aspect_ratio": 1.778,
                "file_path": "/pe2APM7NsJXfNRfq2cUWdc0dRbQ.jpg",
                "height": 1280,
                "iso_639_1": "en",
                "width": 1600,
                "vote_average": 3.334,
                "vote_count": 2
            },
            {
                "aspect_ratio": 1.778,
                "file_path": "/pe2APM7NsJXfNRfq2cUWdc0dRbQ.jpg",
                "height": 1280,
                "iso_639_1": "en",
                "width": 1600,
                "vote_average": 3.334,
                "vote_count": 2
            }
        ],
        "posters": [
            {"aspect_ratio": 0.667, "file_path": "/oKiOhsSRWO6fRqxtvda8WuCiXBm.jpg", "height": 2507, "iso_639_1": "en", "width": 500},
            {"aspect_ratio": 0.667, "file_path": "/oKiOhsSRWO6fRqxtvda8WuCiXBm.jpg", "height": 2507, "iso_639_1": "en", "width": 500}
        ]
    }
    mock_response = Mock()
    mock_response.json.return_value = mock_images
    mock_response.status_code = 200

    monkeypatch.setattr(requests, 'get', Mock(return_value=mock_response))

    movie_id = 789
    images_data = get_movie_images(movie_id)

    assert images_data['id'] == mock_images['id']
    assert images_data['backdrops'] == mock_images['backdrops']
    assert images_data['posters'] == mock_images['posters']

    requests.get.assert_called_once_with(
        f"https://api.themoviedb.org/3/movie/{movie_id}/images",
        headers={"Authorization": f"Bearer {api_token}"}
    )

def test_get_single_movie_cast(monkeypatch):
    mock_cast_data = {
        "cast": [
            {"id": 1, "name": "Actor One", "character": "Character One"},
            {"id": 2, "name": "Actor Two", "character": "Character Two"},
            {"id": 3, "name": "Actor Three", "character": "Character Three"},
            {"id": 4, "name": "Actor Four", "character": "Character Four"},
            {"id": 5, "name": "Actor Five", "character": "Character Five"},
            {"id": 6, "name": "Actor Six", "character": "Character Six"},
            {"id": 7, "name": "Actor Seven", "character": "Character Seven"},
            {"id": 8, "name": "Actor Eight", "character": "Character Eight"},
            {"id": 9, "name": "Actor Nine", "character": "Character Nine"},
            {"id": 10, "name": "Actor Ten", "character": "Character Ten"},
            {"id": 11, "name": "Actor Eleven", "character": "Character Eleven"},
            {"id": 12, "name": "Actor Twelve", "character": "Character Twelve"},
            {"id": 13, "name": "Actor Thirteen", "character": "Character Thirteen"}
        ]
    }
    mock_call_tmdb_api = Mock(return_value=mock_cast_data)
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)
    movie_id = 456
    cast_data = get_single_movie_cast(movie_id)
    expected_cast_data = [
        {"id": 1, "name": "Actor One", "character": "Character One"},
        {"id": 2, "name": "Actor Two", "character": "Character Two"},
        {"id": 3, "name": "Actor Three", "character": "Character Three"},
        {"id": 4, "name": "Actor Four", "character": "Character Four"},
        {"id": 5, "name": "Actor Five", "character": "Character Five"},
        {"id": 6, "name": "Actor Six", "character": "Character Six"},
        {"id": 7, "name": "Actor Seven", "character": "Character Seven"},
        {"id": 8, "name": "Actor Eight", "character": "Character Eight"},
        {"id": 9, "name": "Actor Nine", "character": "Character Nine"},
        {"id": 10, "name": "Actor Ten", "character": "Character Ten"},
        {"id": 11, "name": "Actor Eleven", "character": "Character Eleven"},
        {"id": 12, "name": "Actor Twelve", "character": "Character Twelve"}
    ]
    assert cast_data == expected_cast_data
    mock_call_tmdb_api.assert_called_once_with(f"movie/{movie_id}/credits")
