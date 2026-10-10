with orders as (

    select *
    from {{ ref('stg_jaffle_shop__orders') }}

),

customers as (

    select *
    from {{ ref('stg_jaffle_shop__customers') }}

),

orders_with_customers as (

    select
        orders.order_id,
        orders.customer_id,
        customers.first_name,
        customers.last_name,
        orders.order_date,
        orders.status,
        orders._etl_loaded_at

    from orders

    left join customers
        on orders.customer_id = customers.customer_id

)

select *
from orders_with_customers