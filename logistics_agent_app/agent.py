# logistics_agent_app/agent.py

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool
from google.cloud import bigquery


def get_recent_routes(limit: int = 5) -> dict:
    """
    Fetch the most recently logged delivery routes from BigQuery.
    Args:
        limit: Number of recent routes to fetch (default 5)
    """
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
            r"C:\Users\Shambhu Sharan\Desktop\logistic-genai\service_account.json"
        )
        client = bigquery.Client(project="logistics-optimizer-491418")
        query = f"""
            SELECT run_id, timestamp, route, total_distance, num_stops, algorithm
            FROM `logistics-optimizer-491418.logistics_data.routes`
            ORDER BY timestamp DESC
            LIMIT {limit}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        for row in rows:
            if isinstance(row.get("route"), str):
                stops = json.loads(row["route"])
                row["route_readable"] = " → ".join(
                    [s.split(",")[0] for s in stops]
                )
        return {"status": "success", "routes": rows, "count": len(rows)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_route_statistics() -> dict:
    """
    Get aggregate statistics about all logged delivery routes.
    Returns total routes, average distance, max/min distance and avg stops.
    """
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
            r"C:\Users\Shambhu Sharan\Desktop\logistic-genai\service_account.json"
        )
        client = bigquery.Client(project="logistics-optimizer-491418")
        query = """
            SELECT
                COUNT(*)                      AS total_routes,
                ROUND(AVG(total_distance), 1) AS avg_distance_km,
                ROUND(MAX(total_distance), 1) AS max_distance_km,
                ROUND(MIN(total_distance), 1) AS min_distance_km,
                ROUND(AVG(num_stops), 1)      AS avg_stops,
                MAX(timestamp)                AS last_run
            FROM `logistics-optimizer-491418.logistics_data.routes`
        """
        results = list(client.query(query).result())
        return {"status": "success", "stats": dict(results[0])}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def find_routes_by_location(location: str) -> dict:
    """
    Search for all delivery routes that include a specific Delhi location.
    Args:
        location: Location name to search e.g. 'Saket' or 'Rohini'
    """
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
            r"C:\Users\Shambhu Sharan\Desktop\logistic-genai\service_account.json"
        )
        client = bigquery.Client(project="logistics-optimizer-491418")
        query = f"""
            SELECT run_id, timestamp, route, total_distance, num_stops
            FROM `logistics-optimizer-491418.logistics_data.routes`
            WHERE LOWER(route) LIKE LOWER('%{location}%')
            ORDER BY timestamp DESC
            LIMIT 10
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        for row in rows:
            if isinstance(row.get("route"), str):
                stops = json.loads(row["route"])
                row["route_readable"] = " → ".join(
                    [s.split(",")[0] for s in stops]
                )
        return {"status": "success", "location": location,
                "routes": rows, "count": len(rows)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def optimize_delivery_route(locations: str) -> dict:
    """
    Optimize a new delivery route using Nearest Neighbor + 2-opt algorithm.
    Args:
        locations: Comma-separated Delhi locations
                   e.g. 'Saket, Rohini, Dwarka, Connaught Place'
    """
    try:
        from services.mock_data import get_mock_matrix
        from algorithms.nearest_neighbour import (
            nearest_neighbor_route,
            two_opt_improve,
        )

        stops  = [loc.strip() for loc in locations.split(",")]
        matrix = get_mock_matrix()
        available = list(matrix.keys())

        matched = []
        for stop in stops:
            for key in available:
                if any(w.lower() in key.lower()
                       for w in stop.split() if len(w) > 3):
                    if key not in matched:
                        matched.append(key)
                    break

        if len(matched) < 2:
            return {
                "status":  "error",
                "message": f"Matched only {len(matched)} locations. "
                           f"Try: Saket, Rohini, Dwarka, "
                           f"Connaught Place, Lajpat Nagar"
            }

        route, _  = nearest_neighbor_route(matrix, matched[0], matched)
        best, km  = two_opt_improve(route, matrix)

        return {
            "status":          "success",
            "optimized_route": " → ".join([s.split(",")[0] for s in best]),
            "total_distance":  round(km, 1),
            "num_stops":       len(best) - 2,
            "algorithm":       "Nearest Neighbor + 2-opt",
            "stops_matched":   [s.split(",")[0] for s in matched],
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


root_agent = Agent(
    name="logistics_optimizer_agent",
    model="gemini-2.5-flash",
    description=(
        "An intelligent Delhi logistics assistant that optimizes delivery "
        "routes using graph algorithms and queries real route history "
        "from BigQuery."
    ),
    instruction=(
        "You are a smart logistics assistant for a Delhi delivery company. "
        "You have access to real delivery route data in BigQuery "
        "and can optimize new routes using Dijkstra and Nearest Neighbor "
        "graph algorithms.\n\n"
        "You can:\n"
        "1. Show recent delivery routes from the database\n"
        "2. Give statistics about delivery performance\n"
        "3. Find all routes that went through a specific location\n"
        "4. Optimize a brand new delivery route for given locations\n\n"
        "When showing routes always format as: A → B → C → D\n"
        "Always mention total distance in km and number of stops.\n"
        "Be friendly, concise and specific with numbers.\n"
        "Available Delhi locations: Connaught Place, Lajpat Nagar, "
        "Saket, Dwarka Sector 21, Rohini Sector 3."
    ),
    tools=[
        FunctionTool(get_recent_routes),
        FunctionTool(get_route_statistics),
        FunctionTool(find_routes_by_location),
        FunctionTool(optimize_delivery_route),
    ],
)