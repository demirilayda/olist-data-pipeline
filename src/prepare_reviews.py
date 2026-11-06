"""Build the negative review dataset for the complaint analysis.

Keeps written 1-2 star reviews and joins each one with the order context an
operations manager would ask about: delivery time, delay against the promised
date, product category, seller, customer state and revenue.

Outputs:
    outputs/negative_reviews.csv              all written 1-2 star reviews
    outputs/negative_reviews_sample_1000.csv  fixed-seed random sample for labeling

Usage:
    python src/prepare_reviews.py
"""
import logging
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
SAMPLE_SIZE = 1000
RANDOM_SEED = 42

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_raw():
    names = ["orders", "order_items", "order_reviews", "products", "sellers", "customers"]
    tables = {name: pd.read_csv(DATA_DIR / f"olist_{name}_dataset.csv") for name in names}
    tables["translation"] = pd.read_csv(DATA_DIR / "product_category_name_translation.csv")
    return tables


def negative_reviews(reviews):
    """Written 1-2 star reviews, one per order (the latest answer wins)."""
    reviews = reviews.copy()
    reviews["review_comment_message"] = reviews["review_comment_message"].str.strip()
    reviews = reviews[(reviews["review_score"] <= 2) & (reviews["review_comment_message"].fillna("") != "")]
    reviews = (
        reviews.sort_values("review_answer_timestamp")
        .drop_duplicates("order_id", keep="last")
    )
    reviews["review_text"] = (
        reviews["review_comment_title"].fillna("").str.strip() + " " + reviews["review_comment_message"]
    ).str.strip()
    return reviews[["review_id", "order_id", "review_score", "review_text", "review_creation_date"]]


def order_context(t):
    """One row per order with delivery, product, seller and revenue fields."""
    orders = t["orders"].copy()
    for col in ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]:
        orders[col] = pd.to_datetime(orders[col])

    orders["delivered"] = orders["order_delivered_customer_date"].notna()
    orders["delivery_days"] = (
        orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
    ).dt.days
    # Positive = arrived after the promised date
    orders["delay_days"] = (
        orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
    ).dt.days
    # Unknown (NA) for orders that never arrived
    orders["is_late"] = (orders["delay_days"] > 0).astype("boolean").where(orders["delivered"])

    products = t["products"].merge(t["translation"], on="product_category_name", how="left")
    items = t["order_items"].merge(
        products[["product_id", "product_category_name_english"]], on="product_id", how="left"
    )
    items = items.merge(t["sellers"][["seller_id", "seller_state"]], on="seller_id", how="left")

    revenue = items.groupby("order_id").agg(
        revenue=("price", "sum"),
        freight=("freight_value", "sum"),
        n_items=("order_item_id", "count"),
        n_sellers=("seller_id", "nunique"),
    )
    # The most expensive item decides the order's main category and seller
    main_item = (
        items.sort_values("price", ascending=False)
        .drop_duplicates("order_id")
        .set_index("order_id")[["product_category_name_english", "seller_id", "seller_state"]]
        .rename(columns={"product_category_name_english": "category"})
    )

    orders = orders.merge(t["customers"][["customer_id", "customer_state"]], on="customer_id", how="left")
    orders = orders.join(revenue, on="order_id").join(main_item, on="order_id")
    return orders[[
        "order_id", "order_status", "order_purchase_timestamp", "customer_state",
        "delivered", "delivery_days", "delay_days", "is_late",
        "category", "seller_id", "seller_state", "n_items", "n_sellers", "revenue", "freight",
    ]]


def main():
    t = load_raw()
    reviews = negative_reviews(t["order_reviews"])
    dataset = reviews.merge(order_context(t), on="order_id", how="left")
    dataset["category"] = dataset["category"].fillna("unknown")
    dataset.loc[dataset["n_items"].isna(), "category"] = "no_items"

    OUTPUT_DIR.mkdir(exist_ok=True)
    dataset.to_csv(OUTPUT_DIR / "negative_reviews.csv", index=False)
    sample = dataset.sample(n=SAMPLE_SIZE, random_state=RANDOM_SEED)
    sample.to_csv(OUTPUT_DIR / "negative_reviews_sample_1000.csv", index=False)

    logging.info(f"Negative reviews: {len(dataset):,} (sample: {len(sample):,}, seed {RANDOM_SEED})")
    logging.info(f"Score split: {dataset['review_score'].value_counts().sort_index().to_dict()}")
    logging.info(f"Not delivered: {(~dataset['delivered']).mean():.1%} | Late (of delivered): {dataset['is_late'].mean():.1%}")
    logging.info(f"Revenue of these orders: {dataset['revenue'].sum():,.0f} BRL")


if __name__ == "__main__":
    main()
