# 📈 Market Analytics Platform

> **Cloud-native financial analytics platform** — analyzing stock market performance, trading behavior, and risk metrics across 500+ tickers using a full modern data stack.

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=flat&logo=dbt&logoColor=white)](https://getdbt.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com)
[![Tableau](https://img.shields.io/badge/Tableau-E97627?style=flat&logo=tableau&logoColor=white)](https://tableau.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white)](https://github.com/features/actions)

---

## 🌟 What It Does

A production-grade analytics engineering platform that ingests historical market data for 500+ stock tickers, transforms it through layered dbt models, and delivers executive-level financial dashboards through a live Tableau connection to a cloud-hosted PostgreSQL warehouse.

**Analytical capabilities:**
- Daily return analysis and distribution modeling
- Rolling 30-day volatility (EWMA and standard deviation)
- Moving averages (SMA 20, SMA 50, SMA 200)
- Trend signal generation (momentum indicators)
- Period-over-period performance comparisons
- Ticker-level and portfolio-level KPI reporting

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Data Sources                              │
│         Historical OHLCV market data (500+ tickers)          │
└─────────────────────┬────────────────────────────────────────┘
                      │ Python ETL ingestion
┌─────────────────────▼────────────────────────────────────────┐
│                  Raw Data Layer                               │
│              PostgreSQL / Supabase (cloud-hosted)            │
└─────────────────────┬────────────────────────────────────────┘
                      │ dbt transformations
┌─────────────────────▼────────────────────────────────────────┐
│               dbt Transformation Layers                      │
│   Staging → Intermediate → Mart (analytics-ready models)    │
│   + schema tests + data lineage + documentation             │
└─────────────────────┬────────────────────────────────────────┘
                      │ live connection
┌─────────────────────▼────────────────────────────────────────┐
│                  BI Layer                                    │
│         Tableau dashboards — KPI cards, volatility           │
│         charts, return analysis, trend monitoring           │
└──────────────────────────────────────────────────────────────┘
                      │
          GitHub Actions CI/CD
          (dbt tests on every push)
```

---

## 📦 dbt Model Structure

```
models/
├── staging/
│   ├── stg_market_prices.sql        # Raw OHLCV data cleaned and typed
│   ├── stg_tickers.sql              # Ticker metadata and sector mapping
│   └── schema.yml                   # Source definitions + freshness tests
│
├── intermediate/
│   ├── int_daily_returns.sql        # Daily return calculations per ticker
│   ├── int_rolling_volatility.sql   # 30-day EWMA and std-dev volatility
│   ├── int_moving_averages.sql      # SMA 20/50/200 window calculations
│   └── int_momentum_signals.sql     # Trend signal and momentum indicators
│
└── mart/
    ├── mart_stock_performance.sql   # Final ticker-level performance mart
    ├── mart_portfolio_summary.sql   # Portfolio-level aggregated KPIs
    └── schema.yml                   # dbt tests (unique, not_null, custom)
```

---

## 📊 Key Financial KPIs

| Metric | Description |
|---|---|
| `avg_daily_return` | Average daily percentage return per ticker |
| `rolling_30d_volatility` | Rolling 30-day annualized volatility (EWMA) |
| `sma_20 / sma_50 / sma_200` | Simple moving averages for trend analysis |
| `momentum_signal` | Trend direction indicator (bullish/bearish/neutral) |
| `max_price / min_price` | 52-week high/low per ticker |
| `period_return` | Configurable period-over-period return |

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Ingestion & transformation | Python, pandas, NumPy, SQLAlchemy |
| Data warehouse | PostgreSQL hosted on Supabase |
| Transformation layer | dbt Core (staging, intermediate, mart) |
| Data quality | dbt schema tests (unique, not_null, referential, custom) |
| BI & dashboards | Tableau (live PostgreSQL connection) |
| CI/CD | GitHub Actions (dbt test runs on every push) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- dbt-postgres
- Supabase or local PostgreSQL instance

### Setup
```bash
# Clone and install dependencies
git clone https://github.com/Nanduvasireddy04/Market-Analytics-Platform.git
cd Market-Analytics-Platform
pip install -r requirements.txt

# Configure database connection
cp profiles.yml.example ~/.dbt/profiles.yml
# Edit with your PostgreSQL connection details

# Run ingestion
python src/ingest.py

# Run dbt transformations
dbt deps
dbt run
dbt test
dbt docs generate && dbt docs serve
```

---

## ✅ Data Quality

All mart models are covered by dbt schema tests:
- **Uniqueness** — no duplicate ticker-date combinations
- **Not-null** — price and return fields never null in mart layer
- **Custom tests** — return values within realistic bounds (-50% to +50% daily)
- **Freshness** — source freshness checks on raw price data

CI/CD runs `dbt test` on every push via GitHub Actions — the pipeline is always validated.

---

## 👨‍💻 Author

**Nandu Sai Teja Vasireddy** — [nanduvasireddy.vercel.app](https://nanduvasireddy.vercel.app) · [LinkedIn](https://linkedin.com/in/nandu-sai-teja-vasireddy-330512218)
