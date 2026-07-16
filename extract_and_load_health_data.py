import os
import glob
import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

# Configuration Settings
GCP_PROJECT_ID = 'health-dbt-portfolio'
DATASET_ID = 'raw_synthea'
DATA_FOLDER = r'C:\Users\Asibu\Desktop\projects\dbt-projects\data\raw_synthea'

def process_and_load_synthea():
    """Reads localy raw Synthea data files, processes them, and loads them into BigQuery."""

    # Initialize BigQuery client
    client = bigquery.Client(project=GCP_PROJECT_ID)

    # Ensure the destination dataset exists in BigQuery Sandbox
    dataset_ref = client.dataset(DATASET_ID)
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset '{DATASET_ID}' exists in project '{GCP_PROJECT_ID}'.")
    except NotFound:
        print(f"Dataset '{DATASET_ID}' not found in project '{GCP_PROJECT_ID}'. Creating it now.")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)
        print(f"Dataset '{DATASET_ID}' created.")

    # Find all CSV files in the specified data folder 
    csv_files = glob.glob(os.path.join(DATA_FOLDER, '*.csv'))

    if not csv_files:
        print(f"No CSV files found in the folder '{DATA_FOLDER}'.")
        return
    
    print(f"Found {len(csv_files)} CSV files in the folder '{DATA_FOLDER}'.")

    for file_path in csv_files:
        # Get the table name from the filename (e.g. 'patients.csv' -> 'patients')
        file_name = os.path.basename(file_path)
        table_name = file_name.replace(".csv", "_raw").lower()
        table_ref = dataset_ref.table(table_name)

        print(f"Reading local file: '{file_name}'...")

        # Read the CSV file into a Pandas DataFrame
        # Low_memory=False stops pandas from guessing mixed data types incorrectly
        df = pd.read_csv(file_path, low_memory=False)

        # Simple Data Cleaning step: clean column names (lowercase and replace spaces with underscores)
        df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_' ) for c in df.columns]

        # Configure the BigQuery load job
        job_config = bigquery.LoadJobConfig(
            # WRITE_TRUNCATE will overwrite the table if it already exists
            write_disposition="WRITE_TRUNCATE",
            autodetect=True,  # Let BigQuery auto-detect the (schema) column types(Strings, Integers, Dates)
        )

        print(f"Uploading {len(df)} rows into BigQuery table: {DATASET_ID}.{table_name}...")

        # Stream the data to Google Cloud
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Wait for the database to finish loading the data

        print(f"Successfully loaded {table_name} into BigQuery sandbox.")
    
    print("All Synthea files have been successfully processed and loaded into BigQuery!.")

if __name__ == "__main__":
    try:
        process_and_load_synthea()
    except Exception as e:
        print(f"Pipeline Ingestion Failed: {str(e)}")
