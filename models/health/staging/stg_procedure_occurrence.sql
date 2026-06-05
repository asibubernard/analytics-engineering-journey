with source as (
    select * from {{ source('cms_omop', 'procedure_occurrence') }}
),

renamed as (
    select 
        procedure_occurrence_id,
        person_id as patient_id,
        procedure_concept_id,
        procedure_dat as procedure_date, 
        visit_occurrence_id
    from source
)

select * from renamed