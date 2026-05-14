from typing import Literal

from presentation.api.use_cases.common.response_envelopes import APISuccessResponse

from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.success.dto import VerifyJobSuccessDTO

VerifyJobSuccessResultLiteral = Literal["verification_started"]

class VerifyJobSuccessResponse(APISuccessResponse[VerifyJobSuccessDTO]):
    result: VerifyJobSuccessResultLiteral