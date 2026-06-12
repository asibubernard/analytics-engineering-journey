select condition_concept_id
from {{ ref('stg_condition_occurrence') }}
where condition_concept_id is null