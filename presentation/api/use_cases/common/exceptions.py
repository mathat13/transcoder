from presentation.api.use_cases.common.response_envelopes import APIFailureResponse

class ApplicationFailure(Exception):
    def __init__(self, status_code: int, response: APIFailureResponse):
        self.status_code = status_code
        self.response = response