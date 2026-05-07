with source as (

    select *
    from {{ source('raw', 'raw_stock_prices') }}

),

cleaned as (

    select
        ticker,
        price_date::date as price_date,
        open_price::numeric as open_price,
        high_price::numeric as high_price,
        low_price::numeric as low_price,
        close_price::numeric as close_price,
        adjusted_close::numeric as adjusted_close,
        volume::bigint as volume,
        source,
        ingested_at::timestamptz as ingested_at,
        current_timestamp as transformed_at
    from source

)

select *
from cleaned