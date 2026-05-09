from presentation.api.shared.responses import APIErrorResponse

class APIError(Exception):
    def __init__(self, status_code: int, response: APIErrorResponse):
        self.status_code = status_code
        self.response = response