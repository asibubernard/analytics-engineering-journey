with conditions as (
    select * from {{ ref('stg_condition_occurrence') }}
),
pro_costs as (
    select * from {{ ref('int_procedure_costs') }}
),
concepts as (
    select concept_id, concept_name from {{ source('cms_omop', 'concept') }}
)
select
    cond.condition_concept_id,
    co.concept_name as diagnosis_name,
    cond.patient_id,
    pc.total_charge,
    pc.total_paid
from conditions cond
left join pro_costs pc
    on cond.patient_id = pc.patient_id
    and cond.visit_occurrence_id = pc.visit_occurrence_id
left join concepts co on cond.condition_concept_id = co.concept_id
