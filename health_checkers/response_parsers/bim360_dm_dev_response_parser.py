from health_checkers.response_parsers.bim360_dm_dev_response_parser_base import Bim360DMDevResponseParserBase


class Bim360DMDevResponseParser(Bim360DMDevResponseParserBase):
    def __init__(self):
        good_response_result = 'GOOD'
        super().__init__(good_response_result)
