-- 4. Top 5 Products by Revenue

SELECT
    product_name,
    category,
    SUM(quantity) AS total_quantity_sold,
    COUNT(*) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM retail_sales
GROUP BY
    product_name,
    category
ORDER BY total_revenue DESC
LIMIT 5;