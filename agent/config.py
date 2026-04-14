import os
from dotenv import load_dotenv

load_dotenv()

MAPS_API_KEY  = os.getenv("GOOGLE_MAPS_API_KEY")
GCP_PROJECT   = os.getenv("GOOGLE_CLOUD_PROJECT")
GCP_REGION    = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
BQ_DATASET    = os.getenv("BIGQUERY_DATASET", "logistics_data")
USE_MOCK      = os.getenv("USE_MOCK", "false").lower() == "true"