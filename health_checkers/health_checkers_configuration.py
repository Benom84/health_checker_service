from health_checkers.data_fetchers.url_data_fetcher import UrlDataFetcher
from health_checkers.health_checkers_constants import BIM60DM_DEV_URL, BIM60DM_STAGING_URL, BIM60DM_DEV_COMMANDS_URL
from health_checkers.response_parsers.bim360_dm_commands_dev_response_parser import Bim360DMCommandsDevResponseParser
from health_checkers.response_parsers.bim360_dm_dev_response_parser import Bim360DMDevResponseParser
from health_checkers.response_parsers.bim360_staging_response_parser import Bim360StagingResponseParser

HEALTH_CHECKERS_CONFIGURATION_DICT = {
    BIM60DM_DEV_URL: {
        'parser': Bim360DMDevResponseParser,
        'data_fetcher': UrlDataFetcher,
    },
    BIM60DM_DEV_COMMANDS_URL: {
        'parser': Bim360DMCommandsDevResponseParser,
        'data_fetcher': UrlDataFetcher,
    },
    BIM60DM_STAGING_URL: {
        'parser': Bim360StagingResponseParser,
        'data_fetcher': UrlDataFetcher,
    }
}