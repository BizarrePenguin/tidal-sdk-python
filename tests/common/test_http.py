from tidal_sdk.common.http import HttpResponse


def test_http_response_fields():
    response = HttpResponse(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body=b"{}",
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.body == b"{}"
