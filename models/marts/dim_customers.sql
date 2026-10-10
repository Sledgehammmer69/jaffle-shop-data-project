
with customers as (

    select *
    from {{ ref('stg_jaffle_shop__customers') }}

),

orders as (

    select *
    from {{ ref('fct_orders') }}

),

customer_metrics as (

    select
        customer_id,
        count(order_id) as total_orders,
        sum(successful_payment_amount) as total_successful_payment_amount,
        sum(payment_count) as total_payment_attempts,
        sum(failed_payment_count) as total_failed_payment_attempts

    from orders
    group by customer_id

),

final as (

    select
        customers.customer_id,
        customers.first_name,
        customers.last_name,

        coalesce(customer_metrics.total_orders, 0) as total_orders,
        coalesce(
            customer_metrics.total_successful_payment_amount, 0
        ) as total_successful_payment_amount,
        coalesce(customer_metrics.total_payment_attempts, 0)
            as total_payment_attempts,
        coalesce(customer_metrics.total_failed_payment_attempts, 0)
            as total_failed_payment_attempts

    from customers

    left join customer_metrics
        on customers.customer_id = customer_metrics.customer_id

)

select *
from final
