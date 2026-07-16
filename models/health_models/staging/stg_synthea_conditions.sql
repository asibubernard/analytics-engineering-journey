with source_conditions as (
    select * from {{ source('raw_synthea', 'conditions_raw' )}}
),

renamed as (
    select
        -- Generate a unique Primary key using dbt_utils
        {{ dbt_utils.generate_surrogate_key([
            'patient',
            'encounter',
            'code',
            'start'
        ]) }} as condition_occurrence_id,

        patient as patient_id, 
        encounter as encounter_id,
        code as condition_code,
        description as condition_description,

        -- Cast dates
        cast(start as DATE) as diagnosed_at,
        cast(stop as DATE) as resolved_at

    from source_conditions
)

select * from renamed