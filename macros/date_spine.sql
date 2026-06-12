{% macro date_spine(start_date, end_date) %}
   select date_day 
   from unnest(generate_date_array(
      cast('{{ start_date }}' as date), 
      cast('{{ end_date }}' as date), 
      interval 1 day
      )) as date_day
{% endmacro %}
 