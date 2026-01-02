### Q1: Top 10 products by sales
SELECT 
    `Product Name`,
    SUM(Sales) AS total_sales
FROM orders
GROUP BY `Product Name`
ORDER BY total_sales DESC
LIMIT 10;

