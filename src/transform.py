def transform_data(df_reviews, products_df):
    return df_reviews.merge(products_df, left_on="product_id", right_on="id", how="left")
