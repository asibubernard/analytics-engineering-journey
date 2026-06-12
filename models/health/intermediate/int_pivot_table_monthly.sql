with source as (
    select * from {{ ref('stg_procedure_occurrence') }}
),

pivot_logic as (
    select 
        patient_id ,
        {{ dbt_utils.pivot(
            column='format_date("%Y-%m", procedure_date)',
            values= ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"],
            agg='sum',
            then_value=1,
            else_value=0,
            prefix='visits_'
        ) }}
    from source
    group by 1
)

select * from pivot_logic

