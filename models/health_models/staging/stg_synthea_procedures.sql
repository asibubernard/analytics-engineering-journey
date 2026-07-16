with source_procedures as (
    select * from {{ source('raw_synthea', 'procedures_raw') }}
),

renamed as (
    select
        -- Unique Primary Key (Surrogate Key)
        {{ dbt_utils.generate_surrogate_key([
            'patient', 
            'encounter', 
            'code', 
            'start'
        ]) }} as procedure_occurrence_id,
        
        -- Structural Foreign Keys
        patient as patient_id,
        encounter as encounter_id,
        
        -- Business Logic Columns
        code as procedure_code,
        description as procedure_description,
        reasoncode as reason_code,
        reasondescription as reason_description,
        
        -- Financial Metrics
        cast(base_cost as FLOAT64) as base_cost,
        
        -- Date Conversions 
        cast(start as TIMESTAMP) as procedure_started_at,
        cast(stop as TIMESTAMP) as procedure_ended_at
    from source_procedures
)

select * from renamed