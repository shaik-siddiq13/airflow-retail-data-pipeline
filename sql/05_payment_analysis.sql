-- 5. Payment Method Analysis

SELECT
    payment_method,
    COUNT(*) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM retail_sales
GROUP BY payment_method
ORDER BY total_revenue DESC;