select 
    patient_id,
    birth_date,
    death_date
from {{ ref('stg_synthea_patients')}}
where birth_date > death_date
