from presentation import (
    APISuccessResponse,
    APIFailureResponse,
)

def test_APISuccessResponse_defaults():
    response = APISuccessResponse()

    assert response.model_dump() == {
        "data": {},
        "meta": {},
    }

def test_APIFailureResponse_defaults():
    response = APIFailureResponse()
    
    assert response.model_dump() == {
        "data": None,
        "meta": None,
    }