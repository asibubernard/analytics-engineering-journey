with procedures as (
    select * from {{ ref('stg_procedure_occurrence') }}
),
costs as (
    select * from {{ ref('stg_cost') }}
)
select
    p.procedure_occurrence_id,
    p.patient_id,
    p.visit_occurrence_id,
    p.procedure_concept_id,
    p.procedure_date,
    c.total_charge,
    c.total_paid
from procedures p
left join costs c
    on p.procedure_occurrence_id = c.procedure_occurrence_id
