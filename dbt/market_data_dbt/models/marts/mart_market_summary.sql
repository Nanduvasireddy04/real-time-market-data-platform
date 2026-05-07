WITH performance_data AS (

    SELECT
        *
    FROM {{ ref('mart_stock_performance') }}

),

market_summary AS (

    SELECT

        COUNT(*) AS total_stocks,

        ROUND(
            AVG(daily_return_percent),
            4
        ) AS average_daily_return,

        ROUND(
            AVG(rolling_30_day_volatility),
            4
        ) AS average_market_volatility,

        MAX(daily_return_percent) AS best_daily_return,

        MIN(daily_return_percent) AS worst_daily_return,

        MAX(close_price) AS highest_stock_price,

        MIN(close_price) AS lowest_stock_price,

        SUM(
            CASE
                WHEN trend_signal = 'BULLISH' THEN 1
                ELSE 0
            END
        ) AS bullish_stocks,

        SUM(
            CASE
                WHEN trend_signal = 'BEARISH' THEN 1
                ELSE 0
            END
        ) AS bearish_stocks

    FROM performance_data

)

SELECT
    *,
    CURRENT_TIMESTAMP AS mart_generated_at
FROM market_summary