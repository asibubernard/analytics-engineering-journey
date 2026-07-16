# analytics-engineering-journey
My Analytics Engineering learning journey with dbt, BigQuery, and healthcare data

# Analytics Engineering Portfolio

Hi! I'm Bernard Asibu from Ghana.

## Background
- BSc in Health Information Management  
- Postgraduate Certificate in Management Information Systems (MIS)  
- 2 years as Health Information Officer (patient records, data privacy, health systems)  
- 4 years software development experience  

I want to combine my healthcare knowledge with strong data engineering skills to build reliable analytics pipelines.

## Goal
Get a **remote Analytics Engineer job** — preferably in health-tech, insurance, or any company that needs clean, tested data for decisions.

## My 16-Week Journey
I'm following a self-study path to master the modern data stack:  
SQL → dbt → Airbyte → Prefect → BigQuery → orchestration → production pipelines → healthcare-focused projects.

### Week 1: Analytics Engineering Mindset & Modern Data Stack Overview
**What I learned:**  
- Role of an analytics engineer  
- ELT vs ETL (why ELT is better today)  
- Modern data stack components  
- T-shaped skills, medallion layers (bronze/silver/gold), dbt viewpoint

**What I did:**  
- Created free dbt Cloud developer account  
- Set up this GitHub repo  
- Connected dbt Cloud to BigQuery sandbox (free)  
- Started dbt Fundamentals course (first lessons)

**Screenshots:**  
<img width="1909" height="879" alt="Screenshot 2026-02-04 231218" src="https://github.com/user-attachments/assets/ba369a2f-4a77-4220-aa61-ebc3bff08c89" />
<img width="1910" height="882" alt="Screenshot 2026-02-04 233553" src="https://github.com/user-attachments/assets/ccc9bb16-f654-43a4-a496-664b0c8e6631" />
<img width="1918" height="882" alt="Screenshot 2026-02-04 233409" src="https://github.com/user-attachments/assets/c1fb4d31-1c16-4b82-b758-e58e51db0268" />

### Week 2–3: Advanced SQL & Data Exploration
**What I learned:** 
- Mental Model of SQL
- Window Functions (RANK, LAG/LEAD)
- Aggregations 
- Subqueries & CTEs
- Practiced on Bigquery Public health dataset. 

**What I did:**  
- Wrote and optimized queries



<img width="1919" height="1042" alt="Screenshot 2026-03-19 102606" src="https://github.com/user-attachments/assets/00eed097-a50f-4676-84ef-b39e958de69f" />
<img width="958" height="948" alt="Screenshot 2026-03-31 105947" src="https://github.com/user-attachments/assets/edbd1d15-7f7d-4191-8454-7c7d93085b41" />
<img width="950" height="941" alt="Screenshot 2026-03-25 082029" src="https://github.com/user-attachments/assets/49a8b5ae-22f7-4d13-b631-555ad9f8a085" />

### Week 4: Git and Version Control 
**What I learned:** 
- Learned branches
- PRs
- Merge conflicts 
- Merged first PR

### Week 5–6: Data Modeling Fundamentals
**What I learned:** 
- Star schema (fact & dimension tables) – mental model: library logbook
- Medallion layers (bronze → silver → gold) – mental model: kitchen pantry
- dbt project layers: staging (foundation), intermediate (frame), marts (furnished rooms)
- Difference between ref() and source()
- Writing tests with schema.yml and generating documentation with dbt docs

**What I did:**  
- Built a complete Jaffle Shop pipeline from raw CSV seeds to a daily sales mart
- Applied the same patterns to a public healthcare dataset (CMS SynPUF / OMOP) to create a health analytics pipeline
- Added data quality tests (not_null, unique) and generated a lineage graph

**Jaffle Shop Models**  
- Staging: stg_orders, stg_customers, stg_items
- Intermediate: int_order_details
- Mart: mart_daily_sales

**Healthcare models (bonus sprint)**  
- Staging: stg_person, stg_visit_occurrence
- Intermediate: int_patient_visits
- Mart: mart_patient_cost_summary

**Tech used:**
dbt Core (Bigquery adapter), Google Bigquery sandbox, Git & Github
URL: https://asibubernard.github.io/analytics-engineering-journey/#!/overview

<img width="953" height="482" alt="mart_diagnosis_cost_summary" src="https://github.com/user-attachments/assets/ffa9598c-408b-4ee2-a535-72a58d31822a" />
<img width="941" height="441" alt="mart" src="https://github.com/user-attachments/assets/ffff0e7f-3905-4cd9-9acd-baa53b5184bb" />

## Week 7–8: Intro to dbt & Basic Commands

**What I Learned**
- The core dbt workflow: `dbt run`, `dbt test`, `dbt docs generate`, `dbt build`
- How to define sources (`sources.yml`) so dbt knows where raw data lives
- The difference between view, table, and incremental materialisations
- How to add generic data tests (`not_null`, `unique`, `relationships`) in `schema.yml`
- How to generate and host dbt documentation on GitHub Pages

**What I Built**
- Completed the official **Jaffle Shop** tutorial with 3 staging models, 1 intermediate model, and 1 mart
- Added a `sources.yml` file and applied `not_null` and `unique` tests on primary keys
- Hosted the dbt docs site via the `gh-pages` branch and linked it in the repo
- Practiced a full Git workflow: feature branch → PR → merge after code review

## Week 9–10: dbt Mastery

**What I Learned**
- How to write **Jinja macros** to avoid repeating SQL (DRY principle)
- How to pass **arguments** to macros and return dynamic SQL
- How to use **community packages** (`dbt_utils`, `dbt_expectations`) for advanced tests
- The difference between generic, singular, and custom package tests
- How **incremental models** work and when to use them (merge strategy, `is_incremental()`)
- How to generate dynamic SQL with **Jinja loops** (e.g. monthly pivot tables)
- What a **model contract** is and how it enforces column types and nullability

**What I Built**
- 4 custom macros: `audit_columns`, `mask_phi` (PHI hashing), `categorize_diagnosis` (ICD‑10 categories), `date_spine`
- Increased the test suite from 6 to **15+ tests**, including:
  - `dbt_expectations.expect_column_values_to_be_between` (birth year, stay length)
  - `dbt_expectations.expect_column_values_to_not_be_null` (cost columns)
  - A **custom singular test** to detect null condition codes
  - Referential integrity tests (`relationships`) between related tables
- Converted `stg_cost` to an **incremental model** (`unique_key='cost_id'`, BigQuery‑compatible)
- Created a **Jinja loop model** that pivots monthly procedure counts by patient
- Enforced a **model contract** on `mart_diagnosis_cost_summary` (guaranteed types and not‑null)
- Updated dbt docs and pushed the refreshed lineage graph to GitHub Pages

## Week 11: Full Modern Stack – Ingestion with Airbyte + Python Script (Synthea + FHIR)

**What I Learned**
- How ELT works end‑to‑end: **Extract** (source), **Load** (BigQuery), **Transform** (dbt)
- How to bring external data into BigQuery using **Airbyte Cloud** (as well as custom Python scripts)
- How to configure Airbyte sources (CSV files, FHIR endpoints) and destinations (BigQuery)
- The difference between relational (CSV) and hierarchical (FHIR) healthcare data formats
- How to handle raw data schemas (`raw_synthea`, `raw_fhir`) and define them as dbt sources
- The principle of keeping raw data **untouched** and only transforming it in staging models

**What I Built**
- Ingested **Synthea synthetic patient data** (patients, encounters, conditions, procedures) into BigQuery via Airbyte and python.
- Additionally ingested **FHIR‑formatted patient data** (e.g., Patient, Encounter, Condition resources) into a separate raw dataset
- Defined dbt sources for both `raw_synthea` and `raw_fhir` in `sources.yml`
- Built staging models for both data sources, including:
  - `stg_synthea_patients`, `stg_synthea_encounters`, `stg_synthea_conditions`, `stg_synthea_procedures`
  - `stg_fhir_patients`, `stg_fhir_encounters`, `stg_fhir_conditions`
- Applied data tests (`not_null`, `unique`, `accepted_values`, `relationships`) across both pipelines
- Ensured all models passed and generated a unified dbt docs lineage graph showing both data sources.
<img width="1564" height="954" alt="airbyte_Annotation 2026-07-16 101826" src="https://github.com/user-attachments/assets/415a1bd8-8f66-448a-8375-215d3e56bc20" />
## Week 12: Orchestration & Scheduling with Prefect

**What I Learned**
- Why we need **orchestration**: to automate multi‑step pipelines (ingestion → transformation → notification)
- The concept of a **DAG** (Directed Acyclic Graph) – tasks that run in order with dependencies
- How to use **Prefect** (Python library + cloud UI) to schedule, retry, and monitor workflows
- How to integrate Prefect with dbt Cloud jobs and Airbyte connections
- The value of **alerts** (Slack/email) when pipeline runs fail or succeed

**What I Built**
- A Prefect flow with three tasks:
  1. Trigger Airbyte sync (ingest fresh Synthea data)
  2. Run `dbt build` (all models + tests)
  3. Send a Slack notification on success
- Added **retries** and **scheduling** (daily run) to the flow
- Logged flow runs and captured a screenshot of the DAG in the Prefect UI
- Committed the flow code (`flows/health_pipeline.py`) and updated `requirements.txt`

## Let's Connect
Open to remote Analytics Engineer roles — especially in healthcare, insurance, Pharmacy, or data-driven companies.  
Happy to discuss projects, share code, or chat about opportunities!


LinkedIn: https://www.linkedin.com/in/asibubernard/  

Email: asibubernard@gmail.com / eboasibu@gmail.com /

#AnalyticsEngineering #dbt #DataPipeline #RemoteJobs #HealthcareData #Relocation #VisaSponsorship #DataEngineering
