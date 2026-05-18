import pytest

from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.presenter import IngressPresenter
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.responses.non_success import APIIngressNonSuccessResponse
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.results import Deny
from presentation.api.use_cases.common.response_envelopes import HTTPPresentation

def test_IngressPresenter_with_unsupported_event_type():
    # Setup
    result = Deny(reason="unsupported_event_type")
    
    # Exeution
    response = IngressPresenter.present(result=result)

    # Validation
    assert isinstance(response, HTTPPresentation)
    assert isinstance(response.response, APIIngressNonSuccessResponse)
    assert response.model_dump() == {
        "status_code": 400,
        "response": {
            "reason": "unsupported_event_type"
            },
        }