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
<img width="945" height="1028" alt="Screenshot 2026-04-07 094434" src="https://github.com/user-attachments/assets/b169ef8d-2621-46a6-bfb6-e9d7dab65032" />
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
URL: https://asibubernard.github.io/analytics-engineering-journey/#!/overview?g_v=1

<img width="953" height="482" alt="mart_diagnosis_cost_summary" src="https://github.com/user-attachments/assets/ffa9598c-408b-4ee2-a535-72a58d31822a" />
<img width="941" height="441" alt="mart" src="https://github.com/user-attachments/assets/ffff0e7f-3905-4cd9-9acd-baa53b5184bb" />


## Let's Connect
Open to remote Analytics Engineer roles — especially in healthcare, insurance, Pharmacy, or data-driven companies.  
Happy to discuss projects, share code, or chat about opportunities!


LinkedIn: https://www.linkedin.com/in/asibubernard/  

Email: asibubernard@gmail.com / eboasibu@gmail.com /

#AnalyticsEngineering #dbt #DataPipeline #RemoteJobs #HealthcareData #Relocation #VisaSponsorship #DataEngineering
