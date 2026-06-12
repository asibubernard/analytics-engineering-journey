{% set procedure_months = dbt_utils.get_column_values(
    table=ref('stg_procedure_occurrence'), 
    column='format_date("%Y-%m", procedure_date)'
) %}

with source as (
    select * from {{ ref('stg_procedure_occurrence') }}
),

pivot_logic as (
    select 
        patient_id,
        {{ dbt_utils.pivot(
            column='format_date("%Y-%m", procedure_date)',
            values=procedure_months,
            agg='sum',
            then_value=1,
            else_value=0,
            prefix='visits_'
        ) }}
    from source
    group by 1
)

select * from pivot_logic