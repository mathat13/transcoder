from fastapi.responses import JSONResponse

from presentation.api.use_cases.common.exceptions import ApplicationFailure

def application_failure_handler(
    request,
    exc: ApplicationFailure,
    ) -> JSONResponse:

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.response.model_dump(),
    )