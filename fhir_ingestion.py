from http import client
import os
import json
import requests
import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from pathlib import Path
from datetime import datetime, timezone

# ==========================================
# 1. Configuration
# ==========================================
SOURCE_TYPE = "LOCAL"  # Change this to "API" or "LOCAL"

GCP_PROJECT_ID = "health-dbt-portfolio"  # Project ID
DATASET_ID = "raw_fhir_data_3"             # Dataset ID

# Local Settings
LOCAL_FOLDER = r"C:\Users\Asibu\Desktop\projects\dbt-projects\data\raw_fhir_data"

# API Settings
FHIR_API_URL = "https://hapi.fhir.org/baseR4"

# Map FHIR Resource Types to BigQuery Table Names
RESOURCE_TABLE_MAP = {
    "Patient": "fhir_patients",
    "Encounter": "fhir_encounters",
    "Condition": "fhir_conditions",
    "Procedure": "fhir_procedures",
    "Claim": "fhir_claims"
}

# Define explicit schemas for BigQuery tables
TABLE_SCHEMAS = {
    "fhir_patients": [
        bigquery.SchemaField("patient_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("gender", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("birth_date", "STRING", mode="NULLABLE"),  # Keep as string if FHIR dates vary (YYYY or YYYY-MM-DD)
        bigquery.SchemaField("first_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("last_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("city", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("_ingested_at", "TIMESTAMP", mode="REQUIRED")
    ],
        "fhir_conditions": [
        bigquery.SchemaField("condition_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("patient_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("encounter_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("code", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("display", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("clinical_status", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("onset_date", "STRING", mode="NULLABLE"),  # FHIR dates can be partial (e.g., just "2023"), so STRING is safest before dbt parsing
        bigquery.SchemaField("_ingested_at", "TIMESTAMP", mode="REQUIRED")
    ],
    "fhir_procedures": [
        bigquery.SchemaField("procedure_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("patient_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("encounter_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("code", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("display", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("start_time", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("end_time", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("_ingested_at", "TIMESTAMP", mode="REQUIRED")
    ],
    "fhir_encounters": [
        bigquery.SchemaField("encounter_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("patient_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("status", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("class", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("type_code", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("type_display", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("start_time", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("end_time", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("_ingested_at", "TIMESTAMP", mode="REQUIRED")
    ],
    "fhir_claims": [
        bigquery.SchemaField("claim_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("patient_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("total_cost", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("item_count", "INT64", mode="NULLABLE"),
        bigquery.SchemaField("_ingested_at", "TIMESTAMP", mode="REQUIRED")
    ]
    
}

# ==========================================
# 2. FLATTENING FUNCTIONS 
# ==========================================

def safe_extract_code(codeable_concept):
    """Helper to extract the first coding code and display from a FHIR CodeableConcept."""
    if not codeable_concept: return None, None
    coding = codeable_concept.get("coding", [])
    if coding:
        return coding[0].get("code"), coding[0].get("display")
    return None, codeable_concept.get("text")

def flatten_patient(resource):
    names = resource.get("name", [])
    first_name = names[0].get("given", [""])[0] if names else None
    last_name = names[0].get("family") if names else None
    addresses = resource.get("address", [])
    city = addresses[0].get("city") if addresses else None
    return {
        "patient_id": resource.get("id"),
        "gender": resource.get("gender"),
        "birth_date": resource.get("birthDate"),
        "first_name": first_name,
        "last_name": last_name,
        "city": city,
        "_ingested_at": datetime.now(timezone.utc).isoformat()
    }

def flatten_encounter(resource):
    subject_ref = resource.get("subject", {}).get("reference", "")
    patient_id = subject_ref.split("/")[-1] if subject_ref else None
    encounter_type = resource.get("type", [{}])[0]
    code, display = safe_extract_code(encounter_type)
    period = resource.get("period", {})
    return {
        "encounter_id": resource.get("id"),
        "patient_id": patient_id,
        "status": resource.get("status"),
        "class": resource.get("class", {}).get("code") if isinstance(resource.get("class"), dict) else resource.get("class"),
        "type_code": code, 
        "type_display": display,
        "start_time": period.get("start"),
        "end_time": period.get("end"),
        "_ingested_at": datetime.now(timezone.utc).isoformat()
    }

def flatten_condition(resource):
    subject_ref = resource.get("subject", {}).get("reference", "")
    patient_id = subject_ref.split("/")[-1] if subject_ref else None
    encounter_ref = resource.get("encounter", {}).get("reference", "")
    encounter_id = encounter_ref.split("/")[-1] if encounter_ref else None
    code, display = safe_extract_code(resource.get("code"))
    # Handle both string and complex object variations of clinicalStatus
    status_obj = resource.get("clinicalStatus")
    status = status_obj.get("coding", [{}])[0].get("code") if isinstance(status_obj, dict) else status_obj    
    return {
        "condition_id": resource.get("id"),
        "patient_id": patient_id,
        "encounter_id": encounter_id,
        "code": code,
        "display": display,
        "clinical_status": status,
        "onset_date": resource.get("onsetDateTime"),
        "_ingested_at": datetime.now(timezone.utc).isoformat()
    }

def flatten_procedure(resource):
    subject_ref = resource.get("subject", {}).get("reference", "")
    patient_id = subject_ref.split("/")[-1] if subject_ref else None
    encounter_ref = resource.get("encounter", {}).get("reference", "")
    encounter_id = encounter_ref.split("/")[-1] if encounter_ref else None
    code, display = safe_extract_code(resource.get("code"))
    period = resource.get("performedPeriod", {})
    return {
        "procedure_id": resource.get("id"),
        "patient_id": patient_id,
        "encounter_id": encounter_id,
        "code": code,
        "display": display,
        "start_time": period.get("start"),
        "end_time": period.get("end"),
        "_ingested_at": datetime.now(timezone.utc).isoformat()
    }

def flatten_claim(resource):
    subject_ref = resource.get("subject", {}).get("reference", "")
    patient_id = subject_ref.split("/")[-1] if subject_ref else None
    items = resource.get("item", [])
    total_cost = sum(item.get("net", {}).get("value", 0) for item in items)
    return {
        "claim_id": resource.get("id"),
        "patient_id": patient_id,
        "total_cost": total_cost,
        "item_count": len(items),
        "_ingested_at": datetime.now(timezone.utc).isoformat()
    }

# Map resource types to their specific flattening functions
FLATTENERS = {
    "Patient": flatten_patient,
    "Encounter": flatten_encounter,
    "Condition": flatten_condition,
    "Procedure": flatten_procedure,
    "Claim": flatten_claim
}

# ==========================================
# 3. DATA RETRIEVAL FUNCTIONS
# ==========================================

def get_local_files():
    """Yields JSON data from local files."""
    folder = Path(LOCAL_FOLDER)
    if not folder.exists():
        print(f"❌ Local folder {LOCAL_FOLDER} does not exist.")
        return
    for file_path in folder.glob("*.json"):
        try:
            with open(file_path, 'r') as f:
                yield json.load(f)
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")

def get_api_data():
    """Yields JSON data from FHIR API with pagination."""
    for resource_type in RESOURCE_TABLE_MAP.keys():
        url = f"{FHIR_API_URL}/{resource_type}"
        params = {"_count": "50"}  # Fetch 50 resources per page
        pages_fetched = 0
        max_pages = 3  # Limit for testing

        while url and pages_fetched < max_pages:
            try: 
                if pages_fetched == 0:
                    response = requests.get(url, params=params)
                else:
                    response = requests.get(url)  # No params for subsequent pages
                
                if response.status_code == 200:
                    data = response.json()
                    yield data

                    links = data.get("link", [])
                    next_link = next((link['url'] for link in links if link.get('relation') == 'next'), None)
                    url = next_link
                    pages_fetched += 1
                else:
                    print(f"❌ API Error fetching {resource_type}: {response.status_code} - {response.text}")
                    break
            except Exception as e:
                print(f"❌ Request failed for {resource_type}: {e}")
                break
               
# ==========================================
# 4. PROCESS AND LOAD
# ==========================================

def process_and_load(source_generator):
    """Common logic to flatten and load data regardless of source."""
    bg_client = bigquery.Client(project=GCP_PROJECT_ID)
    
    # Ensure dataset exists
    dataset_ref = bg_client.dataset(DATASET_ID)
    try:
        bg_client.get_dataset(dataset_ref)
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        bg_client.create_dataset(dataset)
        print(f"✅ Created dataset {DATASET_ID}")
    
    # Collectors for each table 
    collected_data = {table: [] for table in RESOURCE_TABLE_MAP.values()}

    for bundle in source_generator:
        entries = bundle.get("entry", [])
        for entry in entries:
            resource = entry.get("resource", {})
            resource_type = resource.get("resourceType")

            # check if we have a flattener for this resource type
            if resource_type in FLATTENERS:
                try:
                    flat_record = FLATTENERS[resource_type](resource)
                    table_name = RESOURCE_TABLE_MAP[resource_type]
                    collected_data[table_name].append(flat_record)
                except Exception as e:
                    print(f"❌ Error flattening {resource_type}: {e}")

    # Load each table's data into BigQuery
    print("🚀 Loading data into BigQuery...")
    for table_name, records in collected_data.items():
        if not records:
            print(f"⚠️ No records found for {table_name}, skipping load.")
            continue

        table_ref = f"{GCP_PROJECT_ID}.{DATASET_ID}.{table_name}"
        
        # Configure to handle dynamic schema
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND", 
            autodetect=True
            )

        print(f"📦 Loading {len(records)} records into {table_ref}...")
        load_job = bg_client.load_table_from_json(records, table_ref, job_config=job_config)
        load_job.result()  # Wait for the job to complete

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if SOURCE_TYPE == "LOCAL":
        print("📂 Ingesting from Local Folder...")
        process_and_load(get_local_files())
    elif SOURCE_TYPE == "API":
        print("🌐 Ingesting from API...")
        process_and_load(get_api_data())
    else:
        print("❌ Invalid Source Type")