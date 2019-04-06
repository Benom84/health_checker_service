import requests

from health_checkers.data_fetchers.data_fetcher_base import DataFetcherBase

OK_CODE = 200


class UrlDataFetcher(DataFetcherBase):
    @staticmethod
    def fetch(target: str):
        content = None
        response = requests.get(target)
        if response and response.status_code == OK_CODE and response.content:
            content = response.content
        return content


