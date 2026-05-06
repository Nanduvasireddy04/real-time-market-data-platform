import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

TICKERS = [
    "AAPL", "MSFT", "NVDA", "TSLA", "AMZN",
    "GOOGL", "META", "JPM", "SPY", "QQQ"
]

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def ingest_historical_prices():
    all_data = []

    for ticker in TICKERS:
        print(f"Ingesting {ticker}...")

        df = yf.download(
            ticker,
            period="5y",
            interval="1d",
            auto_adjust=False,
            progress=False,
            group_by="column",
            multi_level_index=False,
        )

        if df.empty:
            print(f"No data for {ticker}")
            continue

        df = df.reset_index()

        # Force clean column names
        df.columns = [str(col).strip() for col in df.columns]

        df["ticker"] = ticker
        df["source"] = "yfinance"
        df["ingested_at"] = datetime.now(timezone.utc)

        df = df.rename(
            columns={
                "Date": "price_date",
                "Open": "open_price",
                "High": "high_price",
                "Low": "low_price",
                "Close": "close_price",
                "Adj Close": "adjusted_close",
                "Volume": "volume",
            }
        )

        df = df[
            [
                "ticker",
                "price_date",
                "open_price",
                "high_price",
                "low_price",
                "close_price",
                "adjusted_close",
                "volume",
                "source",
                "ingested_at",
            ]
        ]

        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    output_path = RAW_DIR / "raw_stock_prices.csv"
    final_df.to_csv(output_path, index=False)

    print("✅ Historical ingestion completed")
    print(f"Rows: {len(final_df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    ingest_historical_prices()


# import yfinance as yf
# import pandas as pd
# from pathlib import Path
# from datetime import datetime, timezone

# TICKERS = [
#     "AAPL", "MSFT", "NVDA", "TSLA", "AMZN",
#     "GOOGL", "META", "JPM", "SPY", "QQQ"
# ]

# RAW_DIR = Path("data/raw")
# RAW_DIR.mkdir(parents=True, exist_ok=True)


# def ingest_historical_prices():
#     all_prices = []

#     for ticker in TICKERS:
#         print(f"Ingesting historical prices for {ticker}")

#         df = yf.download(
#             ticker,
#             period="5y",
#             interval="1d",
#             auto_adjust=False,
#             progress=False
#         )

#         if df.empty:
#             print(f"No data returned for {ticker}")
#             continue

#         df = df.reset_index()

#         df["ticker"] = ticker
#         df["source"] = "yfinance"
#         df["ingested_at"] = datetime.now(timezone.utc)

#         df = df.rename(
#             columns={
#                 "Date": "price_date",
#                 "Open": "open_price",
#                 "High": "high_price",
#                 "Low": "low_price",
#                 "Close": "close_price",
#                 "Adj Close": "adjusted_close",
#                 "Volume": "volume",
#             }
#         )

#         df = df[
#             [
#                 "ticker",
#                 "price_date",
#                 "open_price",
#                 "high_price",
#                 "low_price",
#                 "close_price",
#                 "adjusted_close",
#                 "volume",
#                 "source",
#                 "ingested_at",
#             ]
#         ]

#         all_prices.append(df)

#     final_df = pd.concat(all_prices, ignore_index=True)

#     output_path = RAW_DIR / "raw_stock_prices.csv"
#     final_df.to_csv(output_path, index=False)

#     print("Historical price ingestion completed.")
#     print(f"Rows ingested: {len(final_df)}")
#     print(f"Output file: {output_path}")


# if __name__ == "__main__":
#     ingest_historical_prices()