with source_patients as (
    select * from {{ source('raw_synthea', 'patients_raw') }}
),

renamed as (
    select
        id as patient_id,
        
        -- High-Risk PII (Masked for absolute security)
        {{ mask_phi('first') }} as masked_first_name,
        {{ mask_phi('last') }} as masked_last_name,
        {{ mask_phi('ssn') }} as masked_ssn,
        {{ mask_phi('drivers') }} as masked_drivers_license,
        {{ mask_phi('passport') }} as masked_passport,
        
        -- Demographics
        prefix,
        suffix,
        maiden as maiden_name,
        marital as marital_status,
        race,
        ethnicity,
        gender,
        birthplace,
        
        -- Geographic Data
        address,
        city,
        state,
        county,
        zip,
        cast(lat as FLOAT64) as latitude,
        cast(lon as FLOAT64) as longitude,
        
        -- Financial Metrics
        cast(healthcare_expenses as FLOAT64) as total_healthcare_expenses,
        cast(healthcare_coverage as FLOAT64) as total_healthcare_coverage,
        
        -- Date Conversions
        cast(birthdate as DATE) as birth_date,
        cast(deathdate as DATE) as death_date

    from source_patients
)

-- 3. Final Select
select * from renamed