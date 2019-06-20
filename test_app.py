import pytest
from flask import url_for


@pytest.fixture
def app():
    from app import app

    return app


def test_request_response(client):
    """Verify that application works correctly when all supported parameters are passed."""
    data = {"amount": "100", "input_currency": "EUR", "output_currency": "CZK"}

    result = client.get(url_for("converter", **data))

    assert result.status_code == 200
    assert result.get_json() == {
        "input": {"amount": 100.0, "currency": "EUR"},
        "output": {
            "CZK": 2561.9
        },  # Output value might change according to current exchange rates
    }
