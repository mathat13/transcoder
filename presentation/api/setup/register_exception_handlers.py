from fastapi import FastAPI

from presentation.api.exception_handlers.api_error_handler import api_error_handler
from presentation.api.shared.exceptions import APIError

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(APIError, api_error_handler)