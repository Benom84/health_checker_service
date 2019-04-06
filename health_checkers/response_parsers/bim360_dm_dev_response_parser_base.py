import json

from health_checkers.response_parsers.response_parser import ResponseParser


class Bim360DMDevResponseParserBase(ResponseParser):
    def __init__(self, good_response_result: str):
        self.good_response_result = good_response_result

    def overall_health_check_response(self, response: str):
        response_as_dict = json.loads(response)
        return response_as_dict['status']['overall'] == self.good_response_result
