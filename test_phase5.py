# test_phase5.py

from services.bigquery_logger  import log_route, get_recent_routes
from services.bigquery_public  import (
    query_air_quality,
    query_route_history_stats,
    query_nyc_taxi_traffic,
)
from services.mock_data        import get_mock_locations, get_mock_matrix
from algorithms.nearest_neighbour import (
    nearest_neighbor_route,
    two_opt_improve,
)

# ── Build a route using mock data ─────────────────────────────────
locs   = get_mock_locations()
matrix = get_mock_matrix()
labels = [l["address"] for l in locs]

route, _  = nearest_neighbor_route(matrix, labels[0], labels)
best, km  = two_opt_improve(route, matrix)

print("Optimized route:", best)
print("Total distance: ", round(km, 1), "km")

# ── Test 1: Log route to YOUR BigQuery dataset ────────────────────
print("\n--- Test 1: Logging route to BigQuery ---")
success = log_route(
    route=          best,
    total_distance= km,
    algorithm=      "Nearest Neighbor + 2-opt",
    user_message=   "Phase 5 test run",
    briefing=       "Test briefing text",
)
print("Log success:", success)

# ── Test 2: Read back recent routes ──────────────────────────────
print("\n--- Test 2: Recent logged routes ---")
recent = get_recent_routes(limit=5)
if recent:
    for r in recent:
        print(f"  {r['timestamp']} | {r['num_stops']} stops | {r['total_distance']} km")
else:
    print("  No routes found yet")

# ── Test 3: Query public air quality dataset ──────────────────────
print("\n--- Test 3: Delhi air quality (public dataset) ---")
aq_data = query_air_quality("Delhi")
if aq_data:
    for row in aq_data:
        print(f"  {row['location']} — PM2.5: {round(row['avg_value'],1)} {row['unit']}")
else:
    print("  No air quality data returned")

# ── Test 4: Query NYC taxi traffic ────────────────────────────────
print("\n--- Test 4: NYC taxi traffic at 9am (public dataset) ---")
taxi = query_nyc_taxi_traffic(hour=9)
if taxi:
    for row in taxi[:3]:
        print(f"  Zone {row['pickup_location_id']} — {row['trip_count']} trips")
else:
    print("  No taxi data returned")

# ── Test 5: Your route history stats ─────────────────────────────
print("\n--- Test 5: Route history stats ---")
stats = query_route_history_stats()
if stats:
    print(f"  Total routes:    {stats.get('total_routes')}")
    print(f"  Avg distance:    {round(float(stats.get('avg_distance_km', 0)), 1)} km")
    print(f"  Last run:        {stats.get('last_run')}")
else:
    print("  No stats yet (table may be empty)")