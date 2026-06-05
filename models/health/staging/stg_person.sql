with source as (
    select * from {{ source('cms_omop', 'person') }}
),

renamed as (
    select 
        person_id as patient_id,
        year_of_birth,
        month_of_birth,
        gender_concept_id,
        ethnicity_concept_id
    from source
)

select * from renamed