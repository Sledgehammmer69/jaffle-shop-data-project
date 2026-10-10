with orders as (

    select *
    from {{ ref('int_order_payments') }}

),

final as (

    select
        order_id,
        customer_id,
        first_name,
        last_name,
        order_date,
        status as order_status,

        coalesce(successful_payment_amount, 0)
            as successful_payment_amount,

        coalesce(payment_count, 0)
            as payment_count,

        coalesce(successful_payment_count, 0)
            as successful_payment_count,

        coalesce(failed_payment_count, 0)
            as failed_payment_count

    from orders

)

select *
from final