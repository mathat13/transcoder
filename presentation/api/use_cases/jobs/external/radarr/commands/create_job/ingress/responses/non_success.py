from pydantic import BaseModel

from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.results import IngressNonSuccessReason

class APIIngressNonSuccessResponse(BaseModel):
    reason: IngressNonSuccessReason


