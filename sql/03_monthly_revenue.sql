-- 3. Monthly Revenue Analysis

SELECT
    TO_CHAR(order_date, 'YYYY-MM') AS sales_month,
    COUNT(*) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM retail_sales
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY sales_month;