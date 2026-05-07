WITH latest_metrics AS (

    SELECT
        dr.ticker,
        dr.price_date,
        dr.close_price,
        dr.daily_return_percent,
        ma.moving_avg_7_day,
        ma.moving_avg_30_day,
        vol.rolling_30_day_volatility,

        ROW_NUMBER() OVER (
            PARTITION BY dr.ticker
            ORDER BY dr.price_date DESC
        ) AS row_num

    FROM {{ ref('int_daily_returns') }} dr

    LEFT JOIN {{ ref('int_moving_averages') }} ma
        ON dr.ticker = ma.ticker
        AND dr.price_date = ma.price_date

    LEFT JOIN {{ ref('int_volatility') }} vol
        ON dr.ticker = vol.ticker
        AND dr.price_date = vol.price_date

)

SELECT
    ticker,
    price_date,
    close_price,
    daily_return_percent,
    moving_avg_7_day,
    moving_avg_30_day,
    rolling_30_day_volatility,

    CASE
        WHEN moving_avg_7_day > moving_avg_30_day
        THEN 'BULLISH'

        WHEN moving_avg_7_day < moving_avg_30_day
        THEN 'BEARISH'

        ELSE 'NEUTRAL'
    END AS trend_signal,

    CURRENT_TIMESTAMP AS mart_generated_at

FROM latest_metrics
WHERE row_num = 1