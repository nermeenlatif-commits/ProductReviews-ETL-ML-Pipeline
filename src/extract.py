import json
import pandas as pd
import requests

def extract_data(
    reviews_path: str = "data/reviews.jsonl",
    products_url: str = "https://fakestoreapi.com/products",
):
    # 1) Read reviews JSONL into a list of dicts
    reviews = []
    with open(reviews_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                reviews.append(json.loads(line))

    df_reviews = pd.DataFrame(reviews)

    # 2) Call products API and load JSON
    resp = requests.get(products_url, timeout=10)
    resp.raise_for_status()
    products = resp.json()
    df_products = pd.DataFrame(products)

    return df_reviews, df_products



