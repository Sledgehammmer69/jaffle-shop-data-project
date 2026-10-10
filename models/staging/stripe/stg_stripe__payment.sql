with source as (

    select *
    from {{ source('stripe', 'payment') }}

),

renamed as (

    select
        id as payment_id,
        orderid as order_id,
        paymentmethod as payment_method,
        status,
        amount,
        created as payment_created_at,
        _batched_at
    from source

)

select *
from renamed