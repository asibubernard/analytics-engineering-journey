with orders as (
    select * from {{ ref('stg_orders') }}
),

items as (
    select * from {{ ref('stg_items') }}
),

joined as (
    select 
        o.order_id,
        o.customer_id,
        o.order_date,
        o.store_id,
        o.subtotal,
        o.tax_paid,
        o.order_total,
        i.item_id,
        i.product_sku
    from orders o
    left join items i on o.order_id = i.order_id
)

select * from joined
