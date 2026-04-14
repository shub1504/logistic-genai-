# config.py
import os
from dotenv import load_dotenv

load_dotenv()

MAPS_API_KEY    = os.getenv("GOOGLE_MAPS_API_KEY")
GCP_PROJECT     = "logistics-optimizer-491418"   # hardcoded to fix env issue
BQ_DATASET      = os.getenv("BIGQUERY_DATASET", "logistics_data")
BQ_LOCATION     = "US"
ANTHROPIC_KEY   = os.getenv("ANTHROPIC_API_KEY")
GCP_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
USE_MOCK        = False