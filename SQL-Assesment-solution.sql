WITH recent_orders AS (
    SELECT 
        O.order_id,
        O.customer_id,
        O.order_date,
        OI.product_id,
        OI.quantity,
        OI.price_per_unit,
        OI.quantity * OI.price_per_unit AS amount_spent,
        P.category
    FROM 
        Orders O
    JOIN 
        Order_Items OI ON O.order_id = OI.order_id
    JOIN 
        Products P ON OI.product_id = P.product_id
    WHERE 
        O.order_date >= CURDATE() - INTERVAL 1 YEAR
),
customer_spending AS (
    SELECT 
        customer_id,
        SUM(amount_spent) AS total_spent
    FROM 
        recent_orders
    GROUP BY 
        customer_id
),
category_spending AS (
    SELECT 
        customer_id,
        category,
        SUM(amount_spent) AS category_spent
    FROM 
        recent_orders
    GROUP BY 
        customer_id, category
),
most_purchased_category AS (
    SELECT 
        customer_id,
        category AS most_purchased_category,
        category_spent
    FROM (
        SELECT 
            customer_id,
            category,
            category_spent,
            ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY category_spent DESC) AS ranks
        FROM 
            category_spending
    ) ranked
    WHERE 
        ranks = 1
)
SELECT 
    C.customer_id,
    C.customer_name,
    C.email,
    CS.total_spent,
    MPC.most_purchased_category
FROM 
    Customers C
JOIN 
    customer_spending CS ON C.customer_id = CS.customer_id
JOIN 
    most_purchased_category MPC ON C.customer_id = MPC.customer_id
ORDER BY 
    CS.total_spent DESC
LIMIT 5;