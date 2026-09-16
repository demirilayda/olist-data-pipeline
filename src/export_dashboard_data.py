"""
outputs/olist_master.csv'den Power BI dashboard'unun ihtiyac duydugu ozet
CSV'leri uretir (dashboard/data/). Fanout riskine karsi (bir siparisin
birden fazla item/odeme satiri olabilir) once order_id bazinda,
gelir icin de (order_id, order_item_id) bazinda dedup uygulanir.
"""
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MASTER = "outputs/olist_master.csv"
OUT = "dashboard/data/"


def main():
    df = pd.read_csv(MASTER, parse_dates=["order_purchase_timestamp", "order_delivered_customer_date"])

    order_level = df.drop_duplicates(subset="order_id")[
        ["order_id", "customer_unique_id", "customer_state", "order_status",
         "order_purchase_timestamp", "order_delivered_customer_date", "review_score"]
    ].copy()
    order_level["teslimat_gun"] = (
        order_level["order_delivered_customer_date"] - order_level["order_purchase_timestamp"]
    ).dt.days

    items = df.drop_duplicates(subset=["order_id", "product_id", "order_item_id"])[
        ["order_id", "customer_state", "product_category_name_english", "price"]
    ]

    # --- eyalet_teslimat.csv: 27 eyaletin tamami (siparis sayisi, ort. teslimat, gelir) ---
    delivered = order_level[order_level["order_status"] == "delivered"]
    state_orders = delivered.groupby("customer_state").agg(
        siparis_sayisi=("order_id", "nunique"),
        ortalama_teslimat_gun=("teslimat_gun", "mean"),
    ).reset_index()
    state_revenue = items.groupby("customer_state")["price"].sum().reset_index(name="toplam_gelir")
    eyalet = state_orders.merge(state_revenue, on="customer_state", how="left")
    eyalet["ortalama_teslimat_gun"] = eyalet["ortalama_teslimat_gun"].round(2)
    eyalet = eyalet.sort_values("ortalama_teslimat_gun", ascending=False)
    eyalet.to_csv(OUT + "eyalet_teslimat.csv", index=False)
    logging.info(f"eyalet_teslimat.csv guncellendi: {len(eyalet)} eyalet")

    # --- kategori_gelir.csv: 72 kategorinin tamami ---
    kategori = items.groupby("product_category_name_english").agg(
        toplam_gelir=("price", "sum"),
        satis_adedi=("order_id", "count"),
    ).reset_index().rename(columns={"product_category_name_english": "kategori"})
    kategori = kategori.sort_values("toplam_gelir", ascending=False)
    kategori.to_csv(OUT + "kategori_gelir.csv", index=False)
    logging.info(f"kategori_gelir.csv guncellendi: {len(kategori)} kategori")

    # --- musteri_sadakat.csv: tek seferlik vs tekrarli musteri ---
    siparis_sayisi_musteri = order_level.groupby("customer_unique_id")["order_id"].nunique()
    tekrarli = int((siparis_sayisi_musteri > 1).sum())
    tek_seferlik = int((siparis_sayisi_musteri == 1).sum())
    sadakat = pd.DataFrame({
        "musteri_tipi": ["Tek Seferlik", "Tekrarli"],
        "musteri_sayisi": [tek_seferlik, tekrarli],
    })
    sadakat.to_csv(OUT + "musteri_sadakat.csv", index=False)
    logging.info(f"musteri_sadakat.csv olusturuldu: tek seferlik={tek_seferlik}, tekrarli={tekrarli}")

    # --- siparis_durumu.csv: siparis durum dagilimi (created+approved -> Diger) ---
    durum = order_level["order_status"].value_counts().rename_axis("durum").reset_index(name="siparis_sayisi")
    durum["durum"] = durum["durum"].replace({"created": "Diger", "approved": "Diger"})
    durum = durum.groupby("durum", as_index=False)["siparis_sayisi"].sum().sort_values("siparis_sayisi", ascending=False)
    durum.to_csv(OUT + "siparis_durumu.csv", index=False)
    logging.info(f"siparis_durumu.csv olusturuldu: {len(durum)} durum")

    logging.info("Tum dashboard CSV'leri guncellendi.")


if __name__ == "__main__":
    main()
