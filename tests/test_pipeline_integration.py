from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

def test_pipeline_end_to_end():
    df_reviews, products_df = extract_data()
    combined = transform_data(df_reviews, products_df)
    ok = load_data()

    assert len(df_reviews) > 0
    assert len(products_df) > 0
    assert len(combined) == len(df_reviews)
    assert ok is True
