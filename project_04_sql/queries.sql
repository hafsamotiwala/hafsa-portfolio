### Q1: Top 10 products by Total sales
SELECT 
    `Product Name`,
    SUM(Sales) AS total_sales
FROM orders
GROUP BY `Product Name`
ORDER BY total_sales DESC
LIMIT 10;

### Q2: Top 10 products by Quantity Sold
SELECT 
	`Product Name`,
	SUM(Quantity) AS total_quantity_sold
FROM orders
GROUP BY `Product Name`
ORDER BY total_quantity_sold DESC
LIMIT 10;

### Q3: Sales by REgion & Product Category
SELECT
	Region,
    Category,
    SUM(Sales) as total_sales
FROM orders
GROUP BY Region, Category
ORDER BY Region, total_sales DESC;

### Q4: Monthly Sales Trend
SELECT
    DATE_FORMAT(STR_TO_DATE(`Order Date`, '%m/%d/%Y'), '%Y-%m') AS month,
    SUM(Sales) AS total_sales
FROM orders
GROUP BY month
ORDER BY month;

### Q5: Total Profit by Customer Segment
SELECT
	Segment,
    SUM(Profit) AS total_profit
FROM orders
GROUP BY Segment
ORDER BY total_profit DESC;

### Q6: Top 10 Customers by Total Sales
SELECT
	`Customer Name`,
    SUM(Sales) AS total_sales
FROM orders
GROUP BY `Customer Name`
ORDER BY total_sales DESC
LIMIT 10;

### Q7: Customer Lifetime Value (Top 10 Customers)
SELECT
	`Customer Name`,
    SUM(Sales) AS lifetime_value
FROM orders
GROUP BY `Customer Name`
ORDER BY lifetime_value DESC
LIMIT 10;

### Q8: Sales by Ship Mode
SELECT
	`Ship Mode`,
    SUM(Sales) AS total_sales
FROM orders
GROUP BY `Ship Mode`
ORDER BY total_sales DESC;

### Q9: Rolling 3-Month Revenue
SELECT
    DATE_FORMAT(order_date_parsed, '%Y-%m') AS month,
    SUM(Sales) AS monthly_sales,
    SUM(SUM(Sales)) OVER (
        ORDER BY DATE_FORMAT(order_date_parsed, '%Y-%m')
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rolling_3_month_sales
FROM orders
GROUP BY month
ORDER BY month;

### Q10: Churn Proxy - Customers with No Purchases in Last 6 Months
SELECT
    `Customer Name`,
    MAX(order_date_parsed) AS last_purchase_date
FROM orders
GROUP BY `Customer Name`
HAVING MAX(order_date_parsed) < DATE_SUB('2017-12-31', INTERVAL 6 MONTH);

### Q11: Top Customers by Revenue
SELECT
    `Customer Name`,
    SUM(Sales) AS total_sales,
    RANK() OVER(ORDER BY SUM(Sales) DESC) AS revenue_rank
FROM orders
GROUP BY `Customer Name`
ORDER BY revenue_rank
LIMIT 10;

### Q12: Customer Lifetime Value (Cumulative Sales)
SELECT *
FROM (
    SELECT
        `Customer Name`,
        order_date_parsed,
        SUM(Sales) OVER(PARTITION BY `Customer Name` ORDER BY order_date_parsed) AS cumulative_sales
    FROM orders
) AS t
WHERE `Customer Name` IN ('Sean Miller','Tamara Chand','Raymond Buch')
ORDER BY `Customer Name`, order_date_parsed;

### Q14: Inventory Reorder Suggestion
SELECT 
    `Product Name`,
    SUM(Quantity) AS total_sold,
    CASE 
        WHEN SUM(Quantity) < 50 THEN 'Reorder Needed'
        ELSE 'Stock Sufficient'
    END AS reorder_status
FROM orders
GROUP BY `Product Name`
ORDER BY total_sold ASC
LIMIT 20;

### Q15: Sales by State
SELECT
    State,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    COUNT(DISTINCT `Customer ID`) AS total_customers
FROM orders
GROUP BY State
ORDER BY total_sales DESC
LIMIT 20;

### Q16: Bulk Orders (>10 Units per Customer)
WITH BulkOrders AS (
    SELECT 
        `Customer Name`,
        `Product Name`,
        SUM(Quantity) AS total_quantity,
        COUNT(*) AS order_count,
        SUM(Sales) AS total_sales
    FROM orders
    GROUP BY `Customer Name`, `Product Name`
    HAVING total_quantity > 10
)
SELECT *
FROM BulkOrders
ORDER BY total_quantity DESC;

### Q17: Discount Analysis - Products with Highest Average Discounts
SELECT 
    `Product Name`,
    AVG(Discount) AS Avg_Discount,
    SUM(Sales) AS Total_Sales,
    COUNT(*) AS Orders_Count
FROM orders
GROUP BY `Product Name`
ORDER BY Avg_Discount DESC
LIMIT 20;

### Q18: Profit vs Discount Trends - High-Value Products
SELECT 
    `Product Name`,
    SUM(Profit) AS Total_Profit,
    SUM(Sales) AS Total_Sales,
    COUNT(*) AS Orders_Count
FROM orders
GROUP BY `Product Name`
ORDER BY Total_Profit DESC
LIMIT 20;

### Q19: Customer Discount Sensitivity (Discount vs Profit)
SELECT
    `Customer Name`,
    ROUND(AVG(discount), 3) AS avg_discount,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY `Customer Name`
HAVING AVG(discount) > 0
ORDER BY avg_discount DESC
LIMIT 20;

### Q20: Seasonal Sales Patterns by Month & Category
SELECT
    Category,
    DATE_FORMAT(order_date_parsed, '%Y-%m') AS month,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM orders
GROUP BY Category, month
ORDER BY month, total_sales DESC
LIMIT 20;












