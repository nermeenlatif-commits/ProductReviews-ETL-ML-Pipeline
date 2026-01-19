import pandas as pd

def extract_data():
    """
    Minimal extract step for the coursework scaffold:
    returns two DataFrames (reviews, products) matching the pipeline contract.
    """
    df_reviews = pd.DataFrame(
        [
            {"product_id": 1, "rating": 5, "review": "Great"},
            {"product_id": 2, "rating": 3, "review": "OK"},
        ]
    )

    products_df = pd.DataFrame(
        [
            {"id": 1, "title": "Product 1"},
            {"id": 2, "title": "Product 2"},
        ]
    )

    return df_reviews, products_df


