with source_encounters as (
    select * from {{ source('raw_synthea', 'encounters_raw') }}
),

renamed as (
    select
        id as encounter_id,
        
        -- Foreign Keys
        patient as patient_id,
        organization as organization_id,
        provider as provider_id,
        payer as payer_id,
        
        -- Clinical Details
        encounterclass as encounter_class,  -- e.g., inpatient, outpatient, ambulatory
        code as encounter_code,
        description as encounter_description,
        reasoncode as reason_code,
        reasondescription as reason_description,
        
        -- Financial & Cost Metrics
        cast(base_encounter_cost as FLOAT64) as base_encounter_cost,
        cast(total_claim_cost as FLOAT64) as total_claim_cost,
        cast(payer_coverage as FLOAT64) as payer_coverage,
        
        -- Date & Time Conversions
        cast(start as TIMESTAMP) as encounter_started_at,
        cast(stop as TIMESTAMP) as encounter_ended_at

    from source_encounters
)

select * from renamed