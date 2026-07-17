import pandas as pd
import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract():
    """Ham CSV dosyalarini okur."""
    try:
        orders_df = pd.read_csv("data/olist_orders_dataset.csv")
        order_items_df = pd.read_csv("data/olist_order_items_dataset.csv")
        customers_df = pd.read_csv("data/olist_customers_dataset.csv")
        products_df = pd.read_csv("data/olist_products_dataset.csv")
        payments_df = pd.read_csv("data/olist_order_payments_dataset.csv")
        reviews_df = pd.read_csv("data/olist_order_reviews_dataset.csv")
    except FileNotFoundError as e:
        logging.error(f"CSV dosyasi bulunamadi: {e}")
        raise

    dataframeler = {
        "orders": orders_df,
        "order_items": order_items_df,
        "customers": customers_df,
        "products": products_df,
        "payments": payments_df,
        "reviews": reviews_df
    }

    logging.info(f"Extract tamamlandi: {({isim: df.shape for isim, df in dataframeler.items()})}")
    return dataframeler


def transform(dataframeler):
    """Veriyi temizler, birlestirir, yeni metrikler turetir."""
    try:
        orders_df = dataframeler["orders"]
        order_items_df = dataframeler["order_items"]

        siparis_gelir_df = order_items_df.groupby("order_id")["price"].sum().reset_index()
        siparis_gelir_df = siparis_gelir_df.rename(columns={"price": "siparis_toplam_geliri"})

        birlesik_df = orders_df.merge(siparis_gelir_df, on="order_id", how="left")

        birlesik_df["order_purchase_timestamp"] = pd.to_datetime(birlesik_df["order_purchase_timestamp"])
        birlesik_df["order_delivered_customer_date"] = pd.to_datetime(birlesik_df["order_delivered_customer_date"])
        birlesik_df["order_estimated_delivery_date"] = pd.to_datetime(birlesik_df["order_estimated_delivery_date"])

        birlesik_df["teslimat_suresi_gun"] = (
            birlesik_df["order_delivered_customer_date"] - birlesik_df["order_purchase_timestamp"]
        ).dt.days

        birlesik_df["teslimat_performans_skoru"] = (
            birlesik_df["order_estimated_delivery_date"] - birlesik_df["order_delivered_customer_date"]
        ).dt.days
    except KeyError as e:
        logging.error(f"Beklenen kolon bulunamadi: {e}")
        raise

    logging.info(f"Transform tamamlandi. Sonuc shape: {birlesik_df.shape}")
    return birlesik_df


def load(islenmis_df):
    """Sonucu SQLite/Parquet/CSV olarak kaydeder."""
    try:
        connection = sqlite3.connect("outputs/olist.db")
        islenmis_df.to_sql("etl_sonuc", connection, if_exists="replace", index=False)
        connection.close()
    except sqlite3.Error as e:
        logging.error(f"Veritabanina yazma hatasi: {e}")
        raise

    logging.info("Load tamamlandi. 'etl_sonuc' tablosu outputs/olist.db icine yazildi.")

if __name__ == "__main__":
    logging.info("ETL pipeline basliyor...")

    ham_veri = extract()
    islenmis_veri = transform(ham_veri)
    load(islenmis_veri)

    logging.info("ETL pipeline basariyla tamamlandi.")