-- 8. Highest Revenue Product in Each Category

WITH product_revenue AS (
    SELECT
        category,
        product_name,
        SUM(revenue) AS total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY SUM(revenue) DESC
        ) AS ranking
    FROM retail_sales
    GROUP BY category, product_name
)

SELECT
    category,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue
FROM product_revenue
WHERE ranking = 1
ORDER BY total_revenue DESC;