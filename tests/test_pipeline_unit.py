import pandas as pd
from src.transform import transform_data

def test_transform_data_adds_product_title_and_keeps_rows():
    df_reviews = pd.DataFrame([{"product_id": 1, "rating": 5}])
    products_df = pd.DataFrame([{"id": 1, "title": "Product 1"}])

    out = transform_data(df_reviews, products_df)

    assert "title" in out.columns
    assert out.loc[0, "title"] == "Product 1"
    assert len(out) == len(df_reviews)
