from health_checkers.response_parsers.response_parser import ResponseParser


class MockResponseParser(ResponseParser):
    def __init__(self):
        self.return_value = True

    def overall_health_check_response(self, response: str):
        return self.return_value

    def set_return_value_to_true(self):
        self.return_value = True

    def set_return_value_to_false(self):
        self.return_value = False
