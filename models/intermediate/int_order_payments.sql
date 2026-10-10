with orders as (

    select *
    from {{ ref('int_orders') }}

),

payments as (

    select
        order_id,

        sum(
            case
                when lower(status) = 'success' then amount
                else 0
            end
        ) as successful_payment_amount,

        count(payment_id) as payment_count,

        count_if(lower(status) = 'success') as successful_payment_count,

        count_if(lower(status) = 'fail') as failed_payment_count

    from {{ ref('stg_stripe__payment') }}
    group by order_id

),

order_payments as (

    select
        orders.order_id,
        orders.customer_id,
        orders.first_name,
        orders.last_name,
        orders.order_date,
        orders.status,
        payments.successful_payment_amount,
        payments.payment_count,
        payments.successful_payment_count,
        payments.failed_payment_count

    from orders

    left join payments
        on orders.order_id = payments.order_id

)

select *
from order_payments