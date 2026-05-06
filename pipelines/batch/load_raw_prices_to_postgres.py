import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

RAW_FILE_PATH = Path("data/raw/raw_stock_prices.csv")


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )


def load_data():
    if not RAW_FILE_PATH.exists():
        raise FileNotFoundError("Raw data not found. Run ingest_historical_prices.py first.")

    print("Reading CSV...")
    df = pd.read_csv(RAW_FILE_PATH, low_memory=False)

    df["price_date"] = pd.to_datetime(df["price_date"]).dt.date
    df["ingested_at"] = pd.to_datetime(df["ingested_at"], utc=True)

    engine = get_engine()

    print("Connecting to PostgreSQL...")

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))

        conn.execute(text("DROP TABLE IF EXISTS raw.raw_stock_prices;"))

        conn.execute(text("""
            CREATE TABLE raw.raw_stock_prices (
                ticker TEXT,
                price_date DATE,
                open_price NUMERIC,
                high_price NUMERIC,
                low_price NUMERIC,
                close_price NUMERIC,
                adjusted_close NUMERIC,
                volume BIGINT,
                source TEXT,
                ingested_at TIMESTAMPTZ
            );
        """))

    print("Loading data into database...")

    df.to_sql(
        "raw_stock_prices",
        engine,
        schema="raw",
        if_exists="append",
        index=False,
        chunksize=1000,
    )

    print("✅ Data loaded successfully")
    print(f"Rows: {len(df)}")


if __name__ == "__main__":
    load_data()