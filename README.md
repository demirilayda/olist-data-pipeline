# Olist Data Pipeline

## Project Overview
End-to-end big data pipeline built on the Olist Brazilian E-Commerce dataset.
Covers data exploration, SQL analysis, PySpark transformations, and an ETL pipeline.

## Dataset
- Source: Kaggle - Brazilian E-Commerce Public Dataset by Olist
- ~100K orders, 9 CSV files
- Period: 2016 - 2018

## Technologies Used
- Python, Pandas, Matplotlib, Seaborn
- SQLite, SQL
- PySpark
- Jupyter Notebook
- Git & GitHub

## Project Structure
olist-data-pipeline/
├── README.md
├── requirements.txt
├── data/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_sql_analysis.ipynb
│   └── 03_spark_transformations.ipynb
├── src/
│   └── etl_pipeline.py
└── outputs/

## Setup & Installation
1. Repoyu klonlayin:
git clone https://github.com/demirilayda/olist-data-pipeline.git
cd olist-data-pipeline
2. Gerekli kutuphaneleri kurun:
pip install -r requirements.txt
3. [Kaggle - Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) veri setini indirip `data/` klasorune yerlestirin.
4. Jupyter Notebook'lari sirasiyla calistirin:
   - `01_eda.ipynb`
   - `02_sql_analysis.ipynb`
   - `03_spark_transformations.ipynb`

5. ETL pipeline'ini komut satirindan calistirmak icin:
python src/etl_pipeline.py

## Findings & Business Recommendations

### Key Findings
- Credit card is the dominant payment method (74% of transactions, 78% of revenue) with the highest average order value (163.32).
- `health_beauty` and `watches_gifts` are the top revenue categories; watches_gifts generates similar revenue with far fewer sales, indicating a higher price point.
- Northern states (RR, AP, AM) have significantly longer delivery times (27-29 days) compared to other regions.
- There is a strong inverse relationship between delivery time and customer satisfaction: 1-star orders take nearly twice as long to deliver as 5-star orders (21.3 vs 10.7 days).
- Only ~3.1% of unique customers (2997 out of 96096) made repeat purchases.

### Recommendations
1. **Reduce delivery times** — Given the strong link between delivery speed and satisfaction, investing in logistics improvements could directly boost customer ratings.
2. **Regional logistics partnerships for northern states** — Establishing regional warehouses/partnerships for RR, AP, AM could shorten delivery times and encourage order growth in underserved regions.
3. **Customer loyalty program** — With repeat purchase rate at only ~3.1%, a loyalty/CRM initiative could improve customer retention and reduce reliance on new customer acquisition.


## Contact
ilayda Demir 
ikizogluilayda@gmail.com
