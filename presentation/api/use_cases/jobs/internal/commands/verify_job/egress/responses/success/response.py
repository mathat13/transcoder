from typing import (
    Literal,
    Union,
)

from presentation.api.use_cases.common.response_envelopes import APISuccessResponse

from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.success.dtos import VerificationStartedDTO

VerificationStartedResultLiteral = Literal["verification_started"]

class VerificationStartedResponse(APISuccessResponse[VerificationStartedDTO]):
    result: VerificationStartedResultLiteral

VerifyJobSuccessResponse = Union[VerificationStartedResponse]