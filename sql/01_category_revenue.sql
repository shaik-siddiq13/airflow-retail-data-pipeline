-- 1. Category-wise Revenue Analysis

SELECT
    category,
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM retail_sales
GROUP BY category
ORDER BY total_revenue DESC;