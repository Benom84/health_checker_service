import xml.etree.ElementTree as element_tree

from health_checkers.response_parsers.response_parser import ResponseParser

STAGING_GOOD_TOKEN = 'Good'


class Bim360StagingResponseParser(ResponseParser):
    def __init__(self):
        self.good_response_result = STAGING_GOOD_TOKEN

    def overall_health_check_response(self, response: str):
        root = element_tree.fromstring(response)
        status = root.find('status').text
        return status == self.good_response_result
