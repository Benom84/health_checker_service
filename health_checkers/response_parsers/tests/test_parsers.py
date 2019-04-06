import os

import pytest

from health_checkers.response_parsers.bim360_dm_commands_dev_response_parser import Bim360DMCommandsDevResponseParser
from health_checkers.response_parsers.bim360_dm_dev_response_parser import Bim360DMDevResponseParser
from health_checkers.response_parsers.bim360_staging_response_parser import Bim360StagingResponseParser

current_path = dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.parametrize("checked_parser, file_tested, expected_response", [
    (Bim360DMDevResponseParser, current_path + '/data/bim360dm_dev_good_response.json', True),
    (Bim360DMDevResponseParser, current_path + '/data/bim360dm_dev_bad_response.json', False),
    (Bim360DMCommandsDevResponseParser, current_path + '/data/bim360db_commands_dev_good_response.json', True),
    (Bim360DMCommandsDevResponseParser, current_path + '/data/bim360db_commands_dev_bad_response.json', False),
    (Bim360StagingResponseParser, current_path + '/data/bim360_staging_good_response.xml', True),
    (Bim360StagingResponseParser, current_path + '/data/bim360_staging_bad_response.xml', False),
])
def test_response_parser_response(checked_parser, file_tested, expected_response):
    response_parser = checked_parser()
    with open(file_tested, 'r') as good_response_file:
        data = ''.join(good_response_file.readlines())
    response = response_parser.overall_health_check_response(data)
    assert response is expected_response

