with source as (
    select * from {{ source('cms_omop', 'condition_occurrence') }}
),
renamed as (
    select 
        condition_occurrence_id,
        person_id as patient_id,
        condition_concept_id,
        condition_start_date,
        condition_end_date,
        visit_occurrence_id
    from source
)
select * from renamed