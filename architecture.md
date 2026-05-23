# Real-Time Market Data Engineering & Analytics Platform

A professional end-to-end Data Engineering and Analytics project that ingests historical stock market data, stores it in a cloud warehouse, transforms it using dbt, and visualizes analytics-ready datasets in Tableau executive dashboards.

---

## Project Goal

The goal of this project is to simulate a real-world financial data engineering platform by building a modern analytics pipeline using:

- Python
- PostgreSQL
- dbt
- Supabase (Cloud PostgreSQL)
- Tableau
- Financial Market Data APIs

This project demonstrates:

- Batch data ingestion
- Data warehousing
- ELT architecture
- dbt transformations
- Data quality testing
- Financial analytics modeling
- Cloud-hosted analytics marts
- Executive dashboard engineering

---

## Final Architecture

```txt
Market Data APIs
        ↓
Python Ingestion Pipelines
        ↓
Raw CSV Data Lake Layer
        ↓
PostgreSQL Raw Warehouse Layer
        ↓
dbt Staging Models
        ↓
dbt Intermediate Transformations
        ↓
Analytics Marts
        ↓
Supabase Cloud PostgreSQL
        ↓
Tableau Executive Dashboards
```

---

## Tech Stack

| Layer              | Technology                 |
| ------------------ | -------------------------- |
| Programming        | Python                     |
| Data Source        | yfinance API               |
| Data Storage       | CSV Data Lake              |
| Warehouse          | PostgreSQL                 |
| Cloud Warehouse    | Supabase (PostgreSQL)      |
| Transformation     | dbt Core                   |
| Visualization      | Tableau                    |
| Environment        | Python Virtual Environment |
| ORM / DB Connector | SQLAlchemy                 |
| Data Processing    | pandas                     |

---

## Project Structure

```txt
real-time-market-data-platform/
│
├── data/
│   └── raw/
│
├── pipelines/
│   └── batch/
│
├── db/
│
├── dbt/
│   └── market_data_dbt/
│
├── dashboards/
│
├── docs/
│
├── notebooks/
│
├── requirements.txt
├── .env
└── README.md
```

---

## Day 1 — Project Initialization & Environment Setup

### Objectives

- Initialize project repository
- Create scalable folder structure
- Configure Python environment
- Install core dependencies

### Environment Setup

**Create Virtual Environment**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**Install Dependencies**

```bash
pip install pandas yfinance sqlalchemy psycopg2-binary python-dotenv
```

Generated: `requirements.txt`

---

## Day 2 — Historical Market Data Ingestion Pipeline

### Objective

Build a production-style batch ingestion pipeline that pulls historical stock market data from external APIs.

### Historical Data Pipeline

Created: `pipelines/batch/ingest_historical_prices.py`

### Pipeline Responsibilities

The ingestion pipeline:

- Pulls 5 years of historical stock data
- Connects to the yfinance API
- Collects OHLCV market data
- Normalizes dataframe structure
- Adds ingestion metadata
- Saves clean raw datasets into CSV storage

### Tickers Ingested

`AAPL` · `MSFT` · `NVDA` · `TSLA` · `AMZN` · `GOOGL` · `META` · `JPM` · `SPY` · `QQQ`

### Raw Dataset Schema

| Column         | Description                  |
| -------------- | ---------------------------- |
| ticker         | Stock ticker symbol          |
| price_date     | Trading date                 |
| open_price     | Opening market price         |
| high_price     | Highest market price         |
| low_price      | Lowest market price          |
| close_price    | Closing market price         |
| adjusted_close | Adjusted closing price       |
| volume         | Daily traded volume          |
| source         | Data source                  |
| ingested_at    | Pipeline ingestion timestamp |

### Output Generated

```txt
data/raw/raw_stock_prices.csv
```

**Dataset Size:** 12,560 rows

---

## Day 2 — PostgreSQL Warehouse Layer

### Objective

Build the raw warehouse layer to persist historical market data in PostgreSQL.

### PostgreSQL Setup

- Installed PostgreSQL locally using Homebrew on macOS
- Started PostgreSQL service
- Created warehouse database

```sql
CREATE DATABASE market_data;
```

Environment variables configured via `.env`.

### Raw Warehouse Schema

```txt
raw.raw_stock_prices
```

### Warehouse Loader Pipeline

Created: `pipelines/batch/load_raw_prices_to_postgres.py`

The warehouse loader pipeline:

- Reads normalized CSV datasets
- Connects to PostgreSQL using SQLAlchemy
- Creates schemas and tables
- Loads historical market data into warehouse tables
- Supports scalable ELT architecture

### Data Validation Queries

```sql
SELECT COUNT(*)
FROM raw.raw_stock_prices;
```

```sql
SELECT
    ticker,
    MIN(price_date),
    MAX(price_date),
    COUNT(*)
FROM raw.raw_stock_prices
GROUP BY ticker;
```

---

## Technical Challenges Solved

### SQLAlchemy 2.0 Execution Error

**Issue:** `ObjectNotExecutableError`

**Solution:** Import and wrap raw SQL with `sqlalchemy.text`:

```python
from sqlalchemy import text
```

---

### PostgreSQL Authentication Issue

**Issue:** `role "postgres" does not exist`

**Solution:** Configured PostgreSQL to use the local macOS user role instead of the default `postgres` role.

---

### yfinance MultiIndex / Wide Table Problem

**Issue:** Malformed dataframe columns such as `open_price.1`, `open_price.2`

**Solution:** Flattened yfinance MultiIndex columns and normalized the dataset into warehouse-ready tabular format.

---

## Day 3 — dbt Setup & Staging Models

### Objective

Build the transformation layer using dbt and implement clean staging models with testing.

### dbt Installation

```bash
pip install dbt-core dbt-postgres
```

### Python Compatibility Issue

**Issue:** Compatibility errors using Python 3.14:

```txt
mashumaro.exceptions.UnserializableField
```

**Solution:** Rebuilt the environment using **Python 3.11**, the stable recommended version for modern Data Engineering tools (dbt, Spark, Airflow, Kafka libraries).

### dbt Project Initialization

Created dbt project: `dbt/market_data_dbt`

```bash
dbt debug
# All checks passed
```

---

### dbt Source Layer

Created: `models/staging/sources.yml`

- Registers warehouse tables as dbt sources
- Adds source-level data quality tests
- Enables lineage tracking

---

### Staging Model

Created: `models/staging/stg_stock_prices.sql`

The staging model:

- Casts datatypes
- Standardizes timestamps
- Cleans warehouse records
- Adds transformation timestamps
- Creates reusable analytical base tables

---

### dbt Testing Layer

Created: `models/staging/stg_stock_prices.yml`

Tests added:
- `not_null`
- Source validation tests

```bash
dbt run
dbt test
# All tests passed
```

---

### Current dbt Models (After Day 3)

| Model                | Purpose             |
| -------------------- | ------------------- |
| raw.raw_stock_prices | Raw warehouse table |
| stg_stock_prices     | Clean staging layer |

---

## Day 4 — Intermediate Analytics Engineering Layer

### Objective

Build intermediate analytical transformation models using dbt to create reusable financial analytics datasets. This phase transforms the project from a raw ingestion pipeline into a real analytics engineering platform.

### Intermediate Models Folder Structure

```txt
models/
├── staging/
├── intermediate/
└── marts/
```

---

### Intermediate Model 1 — Daily Returns

**File Created:** `models/intermediate/int_daily_returns.sql`

**Objective:** Calculate daily percentage returns for each stock ticker using historical close prices.

**Business Logic:**

$$\text{Daily Return} = \frac{\text{Close}_t - \text{Close}_{t-1}}{\text{Close}_{t-1}} \times 100$$

This introduces analytical SQL logic commonly used in quantitative analytics, trading systems, portfolio analytics, and financial reporting.

**Key SQL Concepts Used**

- `LAG(close_price)` window function to retrieve the previous trading day's close price
- `PARTITION BY ticker ORDER BY price_date` to calculate independently per ticker in chronological order

**Output Columns**

| Column               | Description                        |
| -------------------- | ---------------------------------- |
| previous_close_price | Previous trading day close         |
| daily_return_percent | Daily percentage gain/loss         |
| trading_day_result   | Gain / Loss / No Change classifier |
| transformed_at       | Transformation timestamp           |

**Trading Day Classification**

| Condition                       | Classification |
| ------------------------------- | -------------- |
| Current close > Previous close  | GAIN           |
| Current close < Previous close  | LOSS           |
| Equal prices                    | NO_CHANGE      |

**Validation Query**

```sql
SELECT *
FROM analytics.int_daily_returns
LIMIT 20;
```

**Sample Output**

| ticker | price_date | daily_return_percent | trading_day_result |
| ------ | ---------- | -------------------- | ------------------ |
| AAPL   | 2021-05-07 | 0.3623               | GAIN               |
| AAPL   | 2021-05-10 | -2.5805              | LOSS               |

---

### Intermediate Model 2 — Moving Averages

**File Created:** `models/intermediate/int_moving_averages.sql`

**Objective:** Calculate rolling moving averages for stock trend analysis — widely used in quantitative finance, trading systems, technical analysis, and trend forecasting.

**SQL Concepts Used**

```sql
-- 7-Day Window
AVG(close_price) OVER (... ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)

-- 30-Day Window
AVG(close_price) OVER (... ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
```

**Output Columns**

| Column            | Description              |
| ----------------- | ------------------------ |
| moving_avg_7_day  | Short-term trend average |
| moving_avg_30_day | Long-term trend average  |

**Validation Query**

```sql
SELECT *
FROM analytics.int_moving_averages
LIMIT 20;
```

---

### Intermediate Model 3 — Volatility Analytics

**File Created:** `models/intermediate/int_volatility.sql`

**Objective:** Calculate rolling stock price volatility using statistical functions.

Volatility measures risk, price instability, market fluctuations, and trading uncertainty — a core quantitative analytics metric.

**SQL Concepts Used**

```sql
STDDEV(daily_return_percent) OVER (... ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
```

**Output Columns**

| Column                    | Description               |
| ------------------------- | ------------------------- |
| rolling_30_day_volatility | 30-day rolling volatility |

**Validation Query**

```sql
SELECT *
FROM analytics.int_volatility
LIMIT 20;
```

---

### Intermediate Layer Summary

| Model               | Purpose                     |
| ------------------- | --------------------------- |
| int_daily_returns   | Daily percentage returns    |
| int_moving_averages | Rolling trend averages      |
| int_volatility      | Risk and volatility metrics |

This phase introduces real analytical engineering concepts including window functions, rolling calculations, statistical analytics, financial metrics, and quantitative transformations — elevating the project significantly beyond beginner ETL work.

---

## Day 5 — Analytics Marts Layer

### Objective

Create business-facing analytics marts optimized for dashboards and reporting tools.

---

### Analytics Mart 1 — Stock Performance Mart

**File Created:** `models/marts/mart_stock_performance.sql`

Combines daily returns, moving averages, volatility metrics, and trend signals into a single dashboard-ready analytics table.

**Metrics Included**

| Metric                    | Purpose              |
| ------------------------- | -------------------- |
| close_price               | Latest stock price   |
| daily_return_percent      | Daily performance    |
| moving_avg_7_day          | Short-term trend     |
| moving_avg_30_day         | Long-term trend      |
| rolling_30_day_volatility | Risk metric          |
| trend_signal              | Bullish/Bearish flag |

**Trend Signal Logic**

- **Bullish:** `MA_7 > MA_30`
- **Bearish:** `MA_7 < MA_30`

This is a common quantitative trading strategy concept.

**SQL Concepts Used:** `ROW_NUMBER()` to retrieve the latest analytical snapshot per ticker.

**Validation Query**

```sql
SELECT *
FROM analytics.mart_stock_performance;
```

---

### Analytics Mart 2 — Market Summary Mart

**File Created:** `models/marts/mart_market_summary.sql`

Creates executive-level market KPIs summarizing the entire analytics platform — simulating executive dashboards, portfolio monitoring systems, and BI reporting platforms.

**Executive KPIs Generated**

| KPI                       | Description               |
| ------------------------- | ------------------------- |
| total_stocks              | Total tracked stocks      |
| average_daily_return      | Average market return     |
| average_market_volatility | Market-wide risk          |
| best_daily_return         | Best performing stock     |
| worst_daily_return        | Worst performing stock    |
| bullish_stocks            | Number of bullish stocks  |
| bearish_stocks            | Number of bearish stocks  |

**Validation Query**

```sql
SELECT *
FROM analytics.mart_market_summary;
```

---

### dbt Documentation & Testing Layer

**Documentation Files Created**

- `models/intermediate/intermediate_models.yml`
- `models/marts/marts.yml`

These YAML files include model descriptions, column descriptions, data quality tests, schema metadata, and documentation support.

**Data Quality Tests Added:** `not_null`, `unique`, schema validation

**dbt Commands Executed**

```bash
dbt test
dbt docs generate
dbt docs serve
```

The generated documentation site includes model lineage graphs, dependencies, test results, model and column descriptions, and full data lineage visualization.

---

## Day 6 — Tableau Dashboard Engineering & Cloud Analytics Visualization

### Objective

Build a professional executive-level financial analytics dashboard using Tableau connected directly to the cloud-hosted PostgreSQL analytics warehouse in Supabase.

This phase completes the project as a full end-to-end Analytics Engineering and BI platform by enabling live analytical reporting, KPI visualization, financial performance monitoring, and interactive dashboard exploration.

---

### Supabase Cloud Migration

The local PostgreSQL analytics warehouse was migrated to **Supabase** (cloud-hosted PostgreSQL), enabling live cloud connectivity for Tableau dashboards.

---

### Tableau Connection Setup

Connected Tableau directly to the Supabase PostgreSQL cloud warehouse using the PostgreSQL connector.

**Connection Configuration**

| Setting   | Value                               |
| --------- | ----------------------------------- |
| Server    | Supabase PostgreSQL Pooler Host     |
| Port      | 6543                                |
| Database  | postgres                            |
| SSL Mode  | Require                             |
| Connector | PostgreSQL                          |

**Connected Analytics Tables**

| Table                             | Purpose                                    |
| --------------------------------- | ------------------------------------------ |
| analytics.mart_stock_performance  | Stock-level analytics and trend metrics    |
| analytics.mart_market_summary     | Executive-level market KPI summaries       |

The Tableau integration enables direct live querying of cloud-hosted analytics marts without manual CSV exports.

---

### Executive Dashboard Engineering

**Dashboard Created:** Vector Market Analytics Dashboard

**Dashboard Objective:** Provide executive-level visibility into financial market performance, stock trends, volatility analytics, and market-wide KPIs using interactive business intelligence visualizations.

---

### Dashboard Components

#### Executive KPI Cards

Built interactive KPI cards displaying:

| KPI                    | Description                    |
| ---------------------- | ------------------------------ |
| Average Daily Return   | Average market performance     |
| Average Market Volatility | Overall market risk indicator |
| Highest Stock Price    | Top-performing stock price     |
| Lowest Stock Price     | Lowest tracked stock price     |

These KPIs simulate executive financial reporting dashboards commonly used in trading analytics platforms, investment monitoring systems, and financial intelligence applications.

---

#### Stock Price Analytics

Created bar chart visualizations showing:

- Close price comparison by ticker
- Relative stock performance analysis
- Comparative market pricing trends

---

#### Daily Return Analytics

Built return analysis dashboards visualizing:

- Daily return percentages
- Positive vs negative market movements
- Comparative return performance by stock ticker

---

#### Rolling Volatility Analytics

Implemented rolling volatility dashboards using 30-day volatility metrics generated in dbt transformation models. This visualization highlights:

- Market instability
- Risk concentration
- Volatility distribution
- Quantitative market risk behavior

---

#### Trend Signal Distribution

Created trend analysis dashboards using bullish and bearish trend classifications generated through moving average crossover logic.

```txt
Bullish → MA_7 > MA_30
Bearish → MA_7 < MA_30
```

This simulates common quantitative trading and technical analysis workflows used in financial analytics systems.

---

#### Detailed Analytics Reporting Table

Built a detailed analytical reporting table displaying:

| Column                    | Description                  |
| ------------------------- | ---------------------------- |
| ticker                    | Stock symbol                 |
| close_price               | Latest close price           |
| daily_return_percent      | Daily percentage return      |
| rolling_30_day_volatility | Volatility risk metric       |
| trend_signal              | Bullish/Bearish classification |

The table supports interactive filtering, dashboard exploration, and ticker-level analytical reporting.

---

### Interactive Dashboard Features

**Global Ticker Filtering**

Implemented dashboard-wide filtering enabling users to dynamically filter all visualizations by stock ticker.

**Cross-Visualization Interactivity**

Configured charts to act as interactive filters — selecting a stock filters all related dashboard metrics and visuals dynamically update across all analytical views.

**Professional Dashboard Formatting**

Applied professional BI dashboard design practices including:

- Executive KPI layouts
- Financial-style color logic
- Minimalist visualization design
- Responsive dashboard structure
- Consistent typography and spacing
- Clean analytical reporting layout

---

### Business Intelligence Engineering Concepts

**Live Cloud Analytics**

The Tableau dashboard queries live analytics marts hosted in Supabase PostgreSQL, simulating real-world BI systems where dashboards connect directly to centralized warehouse layers.

**Analytics Mart Architecture**

The dashboard consumes business-facing dbt marts rather than raw warehouse tables, demonstrating proper analytics engineering layering and semantic modeling principles.

**Financial Analytics Reporting**

The dashboard introduces quantitative analytics concepts including return analytics, rolling volatility calculations, moving average trend analysis, market risk indicators, and executive KPI reporting.

**Interactive BI Workflows**

The dashboard supports dynamic user-driven exploration, enabling real-time analytical slicing, filtering, and comparative financial analysis.

---

## Complete Final Architecture

```txt
Market Data APIs
        ↓
Python ETL Pipelines
        ↓
CSV Raw Data Lake
        ↓
PostgreSQL Warehouse
        ↓
dbt Staging Models
        ↓
Intermediate Financial Analytics Models
        ↓
Analytics Marts
        ↓
Supabase Cloud PostgreSQL
        ↓
Tableau Executive Dashboards
```

---

## Real-World Engineering Concepts

### Data Lake Layer

The raw CSV storage layer acts as a lightweight local data lake, mimicking enterprise architectures where raw source data is stored before transformations are applied.

### ELT Architecture

```txt
Extract → Load → Transform
```

Data is extracted from APIs, loaded into PostgreSQL, then transformed using dbt — mirroring cloud warehouse workflows used in Snowflake, Databricks, BigQuery, and Redshift.

### dbt Transformation Layer

dbt enables modular SQL transformations with reusable models, dependency management, a built-in testing framework, documentation generation, and data lineage visualization.

### Analytics Engineering

The project separates raw data, clean staging models, intermediate business logic, and final analytics marts — improving maintainability, scalability, reusability, and dashboard performance.

### Cloud-Native Analytics Platform

The project simulates modern cloud analytics systems by integrating cloud-hosted PostgreSQL warehousing (Supabase) with live Tableau BI dashboards.

---

## Key Learning Outcomes by Phase

| Phase                      | Skills Learned                                      |
| -------------------------- | --------------------------------------------------- |
| Python ingestion           | API ingestion, pandas, ETL logic                    |
| Raw data storage           | Data lake concepts                                  |
| PostgreSQL warehouse       | SQL warehousing, schema design                      |
| SQLAlchemy                 | Database connectivity                               |
| dbt setup                  | Analytics engineering                               |
| dbt testing                | Data quality validation                             |
| Staging models             | Data cleaning and standardization                   |
| Intermediate models        | Window functions, financial metrics                 |
| Analytics marts            | Business analytics modeling                         |
| dbt docs & testing         | Documentation, lineage, data quality                |
| Supabase cloud migration   | Cloud infrastructure, cloud database integration    |
| Tableau BI engineering     | Dashboarding, KPI reporting, BI visualization       |
| Interactive analytics      | Cross-filtering, dashboard exploration              |

---

## Current Status

**Completed ✅**

- Historical market data ingestion
- PostgreSQL warehouse layer
- dbt staging layer
- Daily returns calculations
- Rolling moving averages
- Volatility analytics
- Analytics marts
- dbt testing
- dbt documentation
- Supabase cloud migration
- Tableau executive dashboards
- Interactive BI reporting
- Financial KPI analytics

**Planned 🔵**

- Kafka streaming
- Airflow orchestration
- Databricks integration
- Snowflake warehouse migration
- ML forecasting models

---

## Potential Enterprise Extensions

### Streaming Architecture

```txt
Kafka → Spark Streaming → Warehouse
```

### Cloud Data Lake

```txt
AWS S3 → Warehouse → dbt → Tableau
```

### Cloud Analytics Architecture

```txt
S3 → Snowflake → dbt Cloud → Tableau
```

### Databricks Integration

- Bronze/Silver/Gold architecture
- Delta Lake tables
- PySpark transformations
- Large-scale financial analytics

### Airflow Orchestration

- Scheduled ingestion jobs
- Automated transformations
- Pipeline monitoring
- Failure alerting

### Machine Learning Extensions

- Financial forecasting models
- Stock trend prediction
- Volatility forecasting
- Risk scoring analytics

---

## Future Extensions

- Kafka streaming ingestion
- Real-time stock pipelines
- Airflow orchestration
- AWS S3 data lake
- Snowflake warehouse
- Databricks transformations
- Dockerized pipelines
- CI/CD deployment
- ML-based financial forecasting

---

## Why This Project Is Resume-Worthy

This project simulates a production-style financial analytics engineering platform using modern cloud-native technologies and industry-standard ELT architecture.

It demonstrates practical experience in:

- Data ingestion engineering
- PostgreSQL warehousing
- dbt analytics engineering
- Financial analytics modeling
- Cloud database infrastructure (Supabase)
- Executive dashboard engineering (Tableau)
- Interactive BI reporting
- End-to-end analytical platform design

The project is highly relevant for roles in **Data Engineering**, **Analytics Engineering**, **BI Engineering**, **Financial Data Engineering**, **Quantitative Analytics**, and **Data Platform Engineering**.

---

## Conclusion

This project establishes a complete end-to-end financial analytics engineering platform capable of ingesting, transforming, modeling, and visualizing market data using modern analytics engineering practices.

By integrating Python ETL pipelines, PostgreSQL warehousing, dbt transformation layers, Supabase cloud infrastructure, and Tableau executive dashboards, the platform demonstrates how production-style cloud analytics systems are designed and implemented in real-world financial analytics environments — creating a portfolio piece that is both production-realistic and interview-ready.
