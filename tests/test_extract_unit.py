import io
import json
import pandas as pd

from src.extract import extract_data


def test_products_api_is_loaded_into_dataframe(mocker):
    """
    PURPOSE OF THIS TEST:

    We want to prove that our extract_data() function correctly:

    1) Reads raw review data from a JSONL file
    2) Calls an external API to get product information
    3) Converts BOTH sources into clean Pandas DataFrames

    We do NOT want this test to depend on:
    - A real file existing on disk
    - The real internet API being available

    So we use MOCKING to fake both parts.
    """

    # ----------------------------------------------------------------------
    # STEP 1 – Create fake JSONL content to simulate a real reviews file
    # ----------------------------------------------------------------------
    fake_jsonl = '{"product_id": 1, "review": "Nice", "rating": 4}\n'

    # ----------------------------------------------------------------------
    # STEP 2 – Create fake API response data
    # This mimics what https://fakestoreapi.com/products would return
    # ----------------------------------------------------------------------
    fake_products = [
        {"id": 10, "title": "T-shirt", "price": 12.99},
        {"id": 11, "title": "Hat", "price": 7.99},
    ]

    # ----------------------------------------------------------------------
    # STEP 3 – Mock the open() function so extract_data() thinks
    # it is reading from a real file
    # ----------------------------------------------------------------------
    mocker.patch(
        "builtins.open",
        return_value=io.StringIO(fake_jsonl)
    )

    # ----------------------------------------------------------------------
    # STEP 4 – Mock the requests.get() call so no real API call happens
    # ----------------------------------------------------------------------
    fake_response = mocker.Mock()
    fake_response.json.return_value = fake_products
    fake_response.raise_for_status.return_value = None

    mocker.patch("requests.get", return_value=fake_response)

    # ----------------------------------------------------------------------
    # STEP 5 – Run the real extract function with our fake dependencies
    # ----------------------------------------------------------------------
    reviews_df, products_df = extract_data()

    # ----------------------------------------------------------------------
    # STEP 6 – Assertions for REVIEWS dataframe
    # ----------------------------------------------------------------------

    # It should be a Pandas DataFrame
    assert isinstance(reviews_df, pd.DataFrame)

    # It should contain the expected columns
    assert list(reviews_df.columns) == ["product_id", "review", "rating"]

    # It should contain exactly one row (from our fake_jsonl)
    assert len(reviews_df) == 1

    # Check the actual data values
    assert reviews_df.iloc[0]["product_id"] == 1
    assert reviews_df.iloc[0]["review"] == "Nice"
    assert reviews_df.iloc[0]["rating"] == 4

    # ----------------------------------------------------------------------
    # STEP 7 – Assertions for PRODUCTS dataframe
    # ----------------------------------------------------------------------

    assert isinstance(products_df, pd.DataFrame)

    # Should contain two products (from fake_products list)
    assert len(products_df) == 2

    # Check individual product titles were loaded correctly
    assert products_df.iloc[0]["title"] == "T-shirt"
    assert products_df.iloc[1]["title"] == "Hat"




