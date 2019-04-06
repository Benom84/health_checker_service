from health_checkers.data_fetchers.data_fetcher_base import DataFetcherBase
from health_checkers.health_checkers_constants import DEFAULT_STATISTICS_SAMPLE_SIZE
from health_checkers.response_parsers.response_parser import ResponseParser


class HealthChecker:

    def __init__(self, target: str,
                 response_parser: ResponseParser,
                 data_fetcher: DataFetcherBase,
                 logger,
                 statistics_sample_size: int = DEFAULT_STATISTICS_SAMPLE_SIZE):
        self.target = target
        self.response_parser = response_parser
        self.data_fetcher = data_fetcher
        self.logger = logger
        self.health_check_samples = list()
        self.statistics_sample_size = statistics_sample_size

    def check_health(self):
        data_content = self.__fetch_data()
        health_check_result = False
        if data_content:
            health_check_result = self.response_parser.overall_health_check_response(data_content)

        return health_check_result

    def get_health_check_statistics(self):
        number_of_checks = min(len(self.health_check_samples), self.statistics_sample_size)
        availability = 0.0

        if self.health_check_samples:
            availability = sum(self.health_check_samples[-1:-self.statistics_sample_size - 1:-1]) / number_of_checks

        return {"availabilityPercentage": availability, "numberOfChecks": number_of_checks}

    def __fetch_data(self):
        content = None

        try:
            content = self.data_fetcher.fetch(self.target)
        except:
            self.logger.exception("Error fetching data from {target}".format(target=self.target))
        finally:

            return content

    def __append_result_to_statistics(self, health_check_status):
        if len(self.health_check_samples) >= self.statistics_sample_size:
            self.health_check_samples.pop(0)
        self.health_check_samples.append(health_check_status)

    def update_health_check_statistics(self):
        health_check_status = self.check_health()
        self.__append_result_to_statistics(health_check_status)
