{% macro categorize_diagnosis(icd_code_column) %}
case
    when {{ icd_code_column }} like 'I%' then 'Cardiovascular'
    when {{ icd_code_column }} like 'E%' then 'Endocrine'
    when {{ icd_code_column }} like 'J%' then 'Respiratory'
    else 'Other'
end as diagnosis_category
{% endmacro %}