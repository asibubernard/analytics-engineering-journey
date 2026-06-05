with diagnosis_costs as (
    select * from {{ ref('int_diagnosis_costs') }}
)

select
    diagnosis_name,
    count(distinct patient_id) as patient_count,
    round(sum(total_paid), 2) as total_paid
from diagnosis_costs
group by diagnosis_name
order by total_paid desc
