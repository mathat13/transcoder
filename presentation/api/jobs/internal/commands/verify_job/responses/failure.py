from typing import Literal

from presentation.api.shared.response_envelopes import APIFailureResponse

from presentation.api.jobs.internal.commands.verify_job.responses.dtos import VerifyJobFailureDTO

VerifyJobFailureResultLiteral = Literal["job_not_found"]

class VerifyJobFailureResponse(APIFailureResponse[VerifyJobFailureDTO]):
    error: VerifyJobFailureResultLiteral