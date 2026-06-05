/* Mart Daily Sales */
with order_details as (
    select * from {{ ref('int_order_details') }}
)

select 
    date(order_date) as order_day,
    count(distinct order_id) as total_orders,
    round(sum(order_total), 2) as total_revenue,
    count(distinct customer_id) as unique_customers
from order_details
group by order_day
order by order_day