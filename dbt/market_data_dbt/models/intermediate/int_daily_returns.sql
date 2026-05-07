WITH stock_prices AS (

    SELECT
        ticker,
        price_date,
        close_price
    FROM {{ ref('stg_stock_prices') }}

),

daily_returns AS (

    SELECT
        ticker,
        price_date,
        close_price,

        LAG(close_price) OVER (
            PARTITION BY ticker
            ORDER BY price_date
        ) AS previous_close_price

    FROM stock_prices

)

SELECT
    ticker,
    price_date,
    close_price,
    previous_close_price,

    ROUND(
        (
            (close_price - previous_close_price)
            / previous_close_price
        ) * 100,
        4
    ) AS daily_return_percent,

    CASE
        WHEN close_price > previous_close_price THEN 'GAIN'
        WHEN close_price < previous_close_price THEN 'LOSS'
        ELSE 'NO_CHANGE'
    END AS trading_day_result,

    CURRENT_TIMESTAMP AS transformed_at

FROM daily_returns
WHERE previous_close_price IS NOT NULL