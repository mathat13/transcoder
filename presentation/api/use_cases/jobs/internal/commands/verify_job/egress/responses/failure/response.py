from typing import Literal

from presentation.api.use_cases.common.response_envelopes import APIFailureResponse

from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.failure.dto import VerifyJobFailureDTO

VerifyJobFailureResultLiteral = Literal["job_not_found"]

class VerifyJobFailureResponse(APIFailureResponse[VerifyJobFailureDTO]):
    error: VerifyJobFailureResultLiteral