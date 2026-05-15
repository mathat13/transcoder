from presentation import (
    APISuccessResponse,
    APIFailureResponse,
)

def test_APISuccessResponse_defaults():
    response = APISuccessResponse()

    assert response.data == {}
    assert response.meta == {}

def test_APIFailureResponse_defaults():
    response = APIFailureResponse()
    
    assert response.data is None
    assert response.meta is None