/*
    Risk Engine Model
    -----------------
    1. Calculates 90-day Moving Averages (Trend).
    2. Calculates Rolling Standard Deviation (Volatility).
    3. Computes Z-Score to flag statistical outliers.
*/

with source_data as (
    select * from {{ ref('raw_sales') }}
),

metrics as (
    select
        suburb,
        sale_date,
        price,
        
        -- Trend: 90-Sale Moving Average
        avg(price) over (
            partition by suburb 
            order by sale_date 
            rows between 89 preceding and current row
        ) as moving_avg_price,

        -- Volatility: 90-Sale Standard Deviation
        stddev(price) over (
            partition by suburb 
            order by sale_date 
            rows between 89 preceding and current row
        ) as rolling_volatility

    from source_data
),

final_risk_scoring as (
    select 
        *,
        -- Z-Score: How many standard deviations away is this price?
        -- Formula: (X - Mean) / StdDev
        case 
            when rolling_volatility is null or rolling_volatility = 0 then 0
            else (price - moving_avg_price) / rolling_volatility 
        end as z_score
    from metrics
)

select 
    *,
    -- Flag Anomalies (Prices +/- 3 Sigma events)
    case 
        when abs(z_score) > 3 then 'ANOMALY' 
        else 'NORMAL' 
    end as risk_category
from final_risk_scoring
order by sale_date desc