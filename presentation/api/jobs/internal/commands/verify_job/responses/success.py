from typing import Literal

from presentation.api.shared.response_envelopes import APISuccessResponse

from presentation.api.jobs.internal.commands.verify_job.responses.dtos import VerifyJobSuccessDTO

VerifyJobSuccessResultLiteral = Literal["verification_started"]

class VerifyJobSuccessResponse(APISuccessResponse[VerifyJobSuccessDTO]):
    result: VerifyJobSuccessResultLiteral