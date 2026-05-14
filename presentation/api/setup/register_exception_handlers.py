from fastapi import FastAPI

from presentation.api.setup.definitions.exception_handlers.application_failure_handler import application_failure_handler
from presentation.api.use_cases.common.exceptions import ApplicationFailure

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationFailure, application_failure_handler)