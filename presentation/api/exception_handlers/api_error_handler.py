from fastapi.responses import JSONResponse

from presentation.api.shared.exceptions import APIError

def api_error_handler(
    request,
    exc: APIError
    ) -> JSONResponse:

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.response.model_dump(),
    )