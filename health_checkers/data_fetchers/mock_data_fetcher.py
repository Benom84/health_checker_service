from health_checkers.data_fetchers.data_fetcher_base import DataFetcherBase


class MockDataFetcher(DataFetcherBase):
    @staticmethod
    def fetch(target: str):
        return target
