-- This test looks for impossible birthdays 
-- If this finds 0 bads rows, test passes!

select 
    id,
    birthdate
from {{ source('raw_synthea', 'patients_raw') }}
where 
    cast(birthdate as DATE) > current_date()
    or cast(birthdate as DATE) < '1900-01-01'