with source as (
    select * from {{ source('cms_omop', 'cost') }}
), 
renamed as (
    select 
        cost_id,
        cost_event_id as procedure_occurrence_id,
        total_charge,
        total_paid
    from source
    where cost_domain_id = 'Procedure'
)
select * from renamed