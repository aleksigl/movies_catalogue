from main import app
from unittest.mock import Mock
import pytest


@pytest.mark.parametrize('list_type, expected_list, expected_endpoint', [
    ('popular', 'popular', 'movie/popular'),
    ('top_rated', 'top_rated', 'movie/top_rated'),
    ('upcoming', 'upcoming', 'movie/upcoming'),
    ('now_playing', 'now_playing', 'movie/now_playing'),
    ('invalid_type', 'popular', 'movie/popular'),
    ('', 'popular', 'movie/popular')
])
def test_homepage(monkeypatch, list_type, expected_list, expected_endpoint):
    api_mock = Mock(return_value={'results': [{'id': i} for i in range(12)]})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)
    with app.test_client() as client:
        response = client.get(f'/?list_type={list_type}')
        assert response.status_code == 200
        api_mock.assert_called_once_with(expected_endpoint)
