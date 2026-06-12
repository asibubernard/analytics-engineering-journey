with source as (
    select * from {{ ref('raw_customers') }}
),

renamed as (
    select 
        id as customer_id,
        name as customer_name,
        {{ audit_columns() }}

    from source
)

select * from renamed 