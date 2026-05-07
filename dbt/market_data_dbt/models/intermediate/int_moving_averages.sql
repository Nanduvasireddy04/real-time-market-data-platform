WITH daily_prices AS (

    SELECT
        ticker,
        price_date,
        close_price
    FROM {{ ref('stg_stock_prices') }}

),

moving_averages AS (

    SELECT
        ticker,
        price_date,
        close_price,

        ROUND(
            AVG(close_price) OVER (
                PARTITION BY ticker
                ORDER BY price_date
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ),
            4
        ) AS moving_avg_7_day,

        ROUND(
            AVG(close_price) OVER (
                PARTITION BY ticker
                ORDER BY price_date
                ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
            ),
            4
        ) AS moving_avg_30_day,

        CURRENT_TIMESTAMP AS transformed_at

    FROM daily_prices

)

SELECT *
FROM moving_averages