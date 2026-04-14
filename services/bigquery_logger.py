# services/bigquery_logger.py

import os 
import json
import uuid
from datetime import datetime
from google.cloud import bigquery
from config import GCP_PROJECT, BQ_DATASET


def get_client() -> bigquery.Client:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        r"C:\Users\Shambhu Sharan\Desktop\logistic-genai\service_account.json"
    )
    return bigquery.Client(project="logistics-optimizer-491418")
def ensure_table_exists(client: bigquery.Client):
    """
    Create the dataset and routes table if they don't exist.
    Safe to call every run — skips if already there.
    """
    # ── Create dataset if missing ──
    dataset_ref = f"{GCP_PROJECT}.{BQ_DATASET}"
    try:
        client.get_dataset(dataset_ref)
    except Exception:
        client.create_dataset(bigquery.Dataset(dataset_ref))
        print(f"[BigQuery] Created dataset: {BQ_DATASET}")

    # ── Create table if missing ──
    table_id = f"{GCP_PROJECT}.{BQ_DATASET}.routes"
    schema = [
        bigquery.SchemaField("run_id",          "STRING",    mode="REQUIRED"),
        bigquery.SchemaField("timestamp",        "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("route",            "STRING",    mode="REQUIRED"),
        bigquery.SchemaField("total_distance",   "FLOAT",     mode="REQUIRED"),
        bigquery.SchemaField("num_stops",        "INTEGER",   mode="REQUIRED"),
        bigquery.SchemaField("algorithm",        "STRING",    mode="REQUIRED"),
        bigquery.SchemaField("user_message",     "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("briefing",         "STRING",    mode="NULLABLE"),
    ]
    try:
        client.get_table(table_id)
    except Exception:
        table = bigquery.Table(table_id, schema=schema)
        client.create_table(table)
        print(f"[BigQuery] Created table: {table_id}")


def log_route(
    route:           list[str],
    total_distance:  float,
    algorithm:       str,
    user_message:    str = "",
    briefing:        str = "",
    run_id:          str = None,
) -> bool:
    """
    Insert one optimized route record into BigQuery.
    Returns True on success, False on failure.
    """
    client = get_client()
    ensure_table_exists(client)

    table_id = f"{GCP_PROJECT}.{BQ_DATASET}.routes"

    row = {
        "run_id":          run_id or str(uuid.uuid4()),
        "timestamp":       datetime.utcnow().isoformat(),
        "route":           json.dumps(route),
        "total_distance":  round(total_distance, 2),
        "num_stops":       len(route) - 2,
        "algorithm":       algorithm,
        "user_message":    user_message,
        "briefing":        briefing,
    }

    errors = client.insert_rows_json(table_id, [row])
    if errors:
        print(f"[BigQuery] Insert errors: {errors}")
        return False

    print(f"[BigQuery] Route logged — {len(route)-2} stops, {round(total_distance,1)} km")
    return True


def get_recent_routes(limit: int = 10) -> list[dict]:
    """
    Fetch the most recently logged routes from your dataset.
    """
    client = get_client()
    query = f"""
        SELECT
            run_id,
            timestamp,
            route,
            total_distance,
            num_stops,
            algorithm
        FROM `{GCP_PROJECT}.{BQ_DATASET}.routes`
        ORDER BY timestamp DESC
        LIMIT {limit}
    """
    try:
        results = client.query(query).result()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"[BigQuery] Could not fetch routes: {e}")
        return []