import io
import pandas as pd
from src.extract import extract_data

def test_extract_handles_empty_reviews_file(mocker):
    mocker.patch("builtins.open", return_value=io.StringIO(""))
    fake_response = mocker.Mock()
    fake_response.json.return_value = []
    fake_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=fake_response)

    reviews_df, products_df = extract_data()

    assert isinstance(reviews_df, pd.DataFrame)
    assert reviews_df.empty
    assert isinstance(products_df, pd.DataFrame)
    assert products_df.empty
