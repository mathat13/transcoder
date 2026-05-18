from presentation.api.use_cases.common.response_envelopes import HTTPPresentation
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.results import Deny
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.responses.non_success import APIIngressNonSuccessResponse
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.results import IngressNonSuccessReason

class IngressPresenter:
    @staticmethod
    def present(result: Deny) -> HTTPPresentation[APIIngressNonSuccessResponse]:
        match result.reason:
            case "unsupported_event_type":
                response = APIIngressNonSuccessResponse(
                    reason=result.reason
                )

                return HTTPPresentation(
                    status_code=400,
                    response=response,
                )
