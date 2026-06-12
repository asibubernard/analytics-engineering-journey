with spine as (
    {{ date_spine('2025-01-01', '2025-12-31') }}
),

daily_visits as (
    select
        cast(procedure_date as date) as visit_date,
        count(*) as num_visits
    from {{ ref('stg_procedure_occurrence') }}
    group by 1 
)

select 
    spine.date_day,
    coalesce(daily_visits.num_visits, 0) as num_visits
from spine
left join daily_visits
    on spine.date_day = daily_visits.visit_date
order by 1 

