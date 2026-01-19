import pandas as pd
from src.extract import extract_data
from src.transform import transform_data


def test_pipeline_end_to_end(mocker):
    # Fake JSONL file content so extract_data() can read it
    fake_jsonl = '{"product_id": 1, "review": "Nice", "rating": 4}\n'

    mocker.patch("builtins.open", mocker.mock_open(read_data=fake_jsonl))

    # Fake API response so extract_data() doesn't call the real internet
    fake_products = [
        {"id": 1, "title": "T-shirt", "price": 12.99},
    ]

    class FakeResp:
        def raise_for_status(self):
            return None

        def json(self):
            return fake_products

    mocker.patch("requests.get", return_value=FakeResp())

    # Run the real pipeline functions
    df_reviews, products_df = extract_data()
    combined_df = transform_data(df_reviews, products_df)

    # Basic checks
    assert isinstance(df_reviews, pd.DataFrame)
    assert isinstance(products_df, pd.DataFrame)
    assert isinstance(combined_df, pd.DataFrame)
    assert len(combined_df) == 1
