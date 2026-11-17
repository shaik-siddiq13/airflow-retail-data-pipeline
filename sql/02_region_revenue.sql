-- 2. Region-wise Revenue Analysis

SELECT
    region,
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM retail_sales
GROUP BY region
ORDER BY total_revenue DESC;