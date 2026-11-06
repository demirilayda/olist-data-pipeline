# Why Do Olist Customers Leave Unhappy?

**In one sentence:** I analyzed ~100K orders from Olist, a Brazilian e-commerce marketplace, to find out what drives bad reviews and why so few customers come back. The results are a Power BI dashboard and three concrete recommendations.

## The Business Questions

| Question | Short answer |
|---|---|
| Does delivery speed affect ratings? | **Yes, strongly.** 1-star orders took 21.3 days to arrive on average; 5-star orders took 10.7. |
| Where are deliveries slowest? | **The northern states** RR, AP and AM wait 27–29 days. |
| Do customers come back? | **Rarely.** Only 3.1% of customers (2,997 of 96,096) ordered again. |
| What sells, and how do people pay? | `health_beauty` and `watches_gifts` lead revenue; credit card brings 78% of it. |
| *Next:* What exactly do 1–2 star customers complain about? | *In progress:* AI-assisted classification of review texts, checked against 100 reviews I labeled by hand. |

## What I Built

```
9 raw CSV files ──► SQL analysis (SQLite) ──► PySpark transformations ──► ETL script ──► Power BI dashboard
```

- **Exploration & SQL:** cleaned and joined orders, payments, reviews, products and sellers.
- **PySpark:** rebuilt the key aggregations so they scale to much larger data.
- **ETL pipeline:** one command builds the master table and the dashboard data.
- **Power BI dashboard:** revenue, delivery and satisfaction views, plus a regional detail page.

## Dataset
- Source: [Kaggle - Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- ~100K orders, 9 CSV files
- Period: 2016 - 2018

## Technologies Used
- Python, Pandas, Matplotlib, Seaborn
- SQLite, SQL
- PySpark
- Power BI
- Jupyter Notebook
- Git & GitHub

## Project Structure
```
olist-data-pipeline/
├── README.md
├── requirements.txt
├── data/                      # raw CSVs (not tracked, download from Kaggle)
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_sql_analysis.ipynb
│   └── 03_spark_transformations.ipynb
├── src/
│   ├── etl_pipeline.py
│   └── export_dashboard_data.py
├── dashboard/
│   ├── olist_dashboard.pbix
│   └── data/                  # tables feeding the dashboard
└── outputs/                   # charts and processed data
```

## Setup & Installation
1. Clone the repository:
   ```
   git clone https://github.com/demirilayda/olist-data-pipeline.git
   cd olist-data-pipeline
   ```
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Download the [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and put the CSV files in the `data/` folder.
4. Run the notebooks in order:
   - `01_eda.ipynb`
   - `02_sql_analysis.ipynb`
   - `03_spark_transformations.ipynb`
5. Run the ETL pipeline from the command line:
   ```
   python src/etl_pipeline.py
   ```

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
İlayda Demir  
ikizogluilayda@gmail.com
