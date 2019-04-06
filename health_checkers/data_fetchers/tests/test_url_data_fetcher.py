import pytest

from health_checkers.data_fetchers.url_data_fetcher import UrlDataFetcher


def test_url_data_fetcher_interface():
    url_data_fetcher = UrlDataFetcher()
    content = url_data_fetcher.fetch('http://www.google.com')
    assert content is not None


def test_url_data_fetcher_exception():
    url_data_fetcher = UrlDataFetcher()
    with pytest.raises(Exception):
        url_data_fetcher.fetch('http://w.m')
