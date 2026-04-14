# services/bigquery_public.py
import os 
from google.cloud import bigquery
from config import GCP_PROJECT


def get_client() -> bigquery.Client:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        r"C:\Users\Shambhu Sharan\Desktop\logistic-genai\service_account.json"
    )
    return bigquery.Client(project="logistics-optimizer-491418")


def query_nyc_taxi_traffic(hour: int = 9) -> list[dict]:
    client = get_client()
    query = f"""
        SELECT
            pickup_location_id,
            COUNT(*)           AS trip_count,
            AVG(trip_distance) AS avg_distance_miles,
            AVG(tip_amount)    AS avg_tip
        FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`
        WHERE EXTRACT(HOUR FROM pickup_datetime) = {hour}
          AND trip_distance > 0
          AND fare_amount   > 0
        GROUP BY pickup_location_id
        ORDER BY trip_count DESC
        LIMIT 10
    """
    print(f"[BQ Public] Querying NYC taxi trips for hour={hour}...")
    try:
        results = client.query(query).result()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"[BQ Public] Taxi query failed: {e}")
        return []


def query_air_quality(city: str = "Delhi") -> list[dict]:
    client = get_client()
    query = f"""
        SELECT
            location,
            city,
            country,
            pollutant,
            AVG(value)         AS avg_value,
            unit,
            MAX(timestamp)     AS latest_reading
        FROM `bigquery-public-data.openaq.global_air_quality`
        WHERE city     = '{city}'
          AND pollutant = 'pm25'
          AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
        GROUP BY location, city, country, pollutant, unit
        ORDER BY avg_value DESC
        LIMIT 5
    """
    print(f"[BQ Public] Querying air quality for {city}...")
    try:
        results = client.query(query).result()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"[BQ Public] Air quality query failed: {e}")
        return []


def query_route_history_stats() -> dict:
    client = get_client()
    query = f"""
        SELECT
            COUNT(*)            AS total_routes,
            AVG(total_distance) AS avg_distance_km,
            MAX(total_distance) AS max_distance_km,
            MIN(total_distance) AS min_distance_km,
            AVG(num_stops)      AS avg_stops,
            MAX(timestamp)      AS last_run
        FROM `{GCP_PROJECT}.logistics_data.routes`
    """
    try:
        results = list(client.query(query).result())
        return dict(results[0]) if results else {}
    except Exception as e:
        print(f"[BQ Public] Stats query failed: {e}")
        return {}