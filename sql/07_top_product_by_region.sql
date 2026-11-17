-- 7. Highest Revenue Product in Each Region

WITH product_revenue AS (
    SELECT
        region,
        product_name,
        SUM(revenue) AS total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY region
            ORDER BY SUM(revenue) DESC
        ) AS ranking
    FROM retail_sales
    GROUP BY region, product_name
)

SELECT
    region,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue
FROM product_revenue
WHERE ranking = 1
ORDER BY total_revenue DESC;