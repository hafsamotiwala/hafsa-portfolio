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






