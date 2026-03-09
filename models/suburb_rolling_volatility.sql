{{ config(materialized='table') }}

WITH monthly_aggregation AS (
    SELECT 
        date_trunc('month', CAST(sale_date AS DATE)) AS sale_month,
        suburb,
        median(CAST(price AS DOUBLE)) AS median_price,
        count(*) AS total_sales
    FROM {{ ref('raw_sales') }}
    GROUP BY 1, 2
)

SELECT 
    sale_month,
    suburb,
    median_price,
    total_sales,
    avg(median_price) OVER (
        PARTITION BY suburb 
        ORDER BY sale_month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rolling_3m_avg_price,
    stddev_samp(median_price) OVER (
        PARTITION BY suburb 
        ORDER BY sale_month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rolling_3m_volatility
FROM monthly_aggregation
ORDER BY suburb, sale_month