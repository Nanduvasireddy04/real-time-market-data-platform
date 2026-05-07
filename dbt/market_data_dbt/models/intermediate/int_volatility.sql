WITH daily_returns AS (

    SELECT
        ticker,
        price_date,
        daily_return_percent
    FROM {{ ref('int_daily_returns') }}

),

volatility AS (

    SELECT
        ticker,
        price_date,
        daily_return_percent,

        ROUND(
            STDDEV(daily_return_percent) OVER (
                PARTITION BY ticker
                ORDER BY price_date
                ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
            ),
            4
        ) AS rolling_30_day_volatility,

        CURRENT_TIMESTAMP AS transformed_at

    FROM daily_returns

)

SELECT *
FROM volatility