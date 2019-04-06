import logging
from unittest.mock import Mock

from health_checkers.data_fetchers.mock_data_fetcher import MockDataFetcher
from health_checkers.health_checker import HealthChecker
from health_checkers.response_parsers.mock_response_parser import MockResponseParser

logger = logging.getLogger()
NUMBER_OF_HEALTH_CHECKS_FOR_TESTS = 5


def setup_health_checker_and_mocks():
    target = 'Arbitrary string'
    response_parser = MockResponseParser()
    data_fetcher = MockDataFetcher()
    health_checker = HealthChecker(target, response_parser, data_fetcher, logger, NUMBER_OF_HEALTH_CHECKS_FOR_TESTS)
    return health_checker, response_parser, data_fetcher


def test_health_checker_good_health_check():
    health_checker, response_parser, data_fetcher = setup_health_checker_and_mocks()
    assert health_checker.check_health() is True


def test_health_checker_bad_health_check():
    health_checker, response_parser, data_fetcher = setup_health_checker_and_mocks()
    response_parser.set_return_value_to_false()
    assert health_checker.check_health() is False


def test_availability_result_when_empty():
    health_checker, response_parser, data_fetcher = setup_health_checker_and_mocks()
    assert health_checker.get_health_check_statistics() == {"availabilityPercentage": 0.0, "numberOfChecks": 0}


def test_availability_result_single_good_sample():
    health_checker, response_parser, data_fetcher = setup_health_checker_and_mocks()
    response_parser.set_return_value_to_true()
    health_checker.update_health_check_statistics()
    assert health_checker.get_health_check_statistics() == {"availabilityPercentage": 1.0, "numberOfChecks": 1}


def test_availability_result_single_bad_sample():
    health_checker, response_parser, data_fetcher = setup_health_checker_and_mocks()
    response_parser.set_return_value_to_false()
    health_checker.update_health_check_statistics()
    assert health_checker.get_health_check_statistics() == {"availabilityPercentage": 0.0, "numberOfChecks": 1}


def test_availability_calculation_20_percent():
    health_checker, response_parser, data_fetcher = setup_health_checker_and_mocks()
    response_parser.set_return_value_to_false()
    for _ in range(NUMBER_OF_HEALTH_CHECKS_FOR_TESTS - 1):
        health_checker.update_health_check_statistics()
    response_parser.set_return_value_to_true()
    health_checker.update_health_check_statistics()

    assert health_checker.get_health_check_statistics() == {"availabilityPercentage": 0.2,
                                                            "numberOfChecks": NUMBER_OF_HEALTH_CHECKS_FOR_TESTS}


def test_availability_calculation_uses_latest_results():
    health_checker, response_parser, data_fetcher = setup_health_checker_and_mocks()
    response_parser.set_return_value_to_false()
    for _ in range(10):
        health_checker.update_health_check_statistics()
    response_parser.set_return_value_to_true()
    for _ in range(2):
        health_checker.update_health_check_statistics()

    assert health_checker.get_health_check_statistics() == {"availabilityPercentage": 0.4,
                                                            "numberOfChecks": NUMBER_OF_HEALTH_CHECKS_FOR_TESTS}


def test_check_health_does_not_raise_exception():
    health_checker, response_parser, data_fetcher = setup_health_checker_and_mocks()
    data_fetcher.fetch = Mock(side_effect=Exception('This should not affect the call'))
    result = health_checker.check_health()
    assert result is False
