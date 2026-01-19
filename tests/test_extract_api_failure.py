import io
import requests
from src.extract import extract_data

def test_extract_raises_if_api_fails(mocker):
    mocker.patch("builtins.open", return_value=io.StringIO('{"product_id": 1, "review": "Nice", "rating": 4}\n'))

    fake_response = mocker.Mock()
    fake_response.raise_for_status.side_effect = requests.HTTPError("API failed")
    mocker.patch("requests.get", return_value=fake_response)

    import pytest
    with pytest.raises(requests.HTTPError):
        extract_data()
