with source_careplans as (
    select * from {{ source('raw_synthea', 'careplans_raw')}}
),

renamed as (
    select 
        id as careplan_id,
        
        -- Foreign Keys 
        patient as patient_id, 
        encounter as encounter_id,

        -- Clinical details
        code as careplan_code,
        description as careplan_description,
        reasoncode as reason_code,
        reasondescription as reason_description,

        -- Date and Time Conversions
        cast(start as TIMESTAMP) as careplan_started_at,
        cast(stop as TIMESTAMP) as careplan_ended_at
    
    from source_careplans    
)

select * from renamed