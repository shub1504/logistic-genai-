from algorithms.graph import Graph
from algorithms.dijkstra import dijkstra, reconstruct_path
from algorithms.nearest_neighbour import nearest_neighbor_route, two_opt_improve
# --- Dijkstra test ---
g = Graph()
g.add_edge("Depot", "WH-1", 4)
g.add_edge("Depot", "WH-2", 2)
g.add_edge("WH-2", "WH-3", 3)
g.add_edge("WH-1", "WH-3", 5)
g.add_edge("WH-2", "WH-1", 6)

dists, preds = dijkstra(g, "Depot")
path = reconstruct_path(preds, "Depot", "WH-3")

print("Shortest distances from Depot:", dists)
print("Shortest path to WH-3:", path)           # expect: Depot → WH-2 → WH-3, cost 5

# --- Nearest Neighbor test ---
dm = {
    "Depot": {"WH-1": 4, "WH-2": 2, "WH-3": 9},
    "WH-1":  {"Depot": 4, "WH-2": 3, "WH-3": 5},
    "WH-2":  {"Depot": 2, "WH-1": 3, "WH-3": 3},
    "WH-3":  {"Depot": 9, "WH-1": 5, "WH-2": 3},
}

route, cost = nearest_neighbor_route(dm, "Depot", ["WH-1", "WH-2", "WH-3"])
print("\nNearest-neighbor route:", route)
print("Route cost:", cost)

improved_route, improved_cost = two_opt_improve(route, dm)
print("2-opt improved route:", improved_route)
print("2-opt cost:", improved_cost)

# --- Phase 3 mock integration test ---
from services.mock_data import get_mock_locations, get_mock_matrix

locations = get_mock_locations()
matrix    = get_mock_matrix()
labels    = [loc["address"] for loc in locations]

from algorithms.nearest_neighbour import nearest_neighbor_route, two_opt_improve

route, cost = nearest_neighbor_route(matrix, labels[0], labels)
improved, improved_cost = two_opt_improve(route, matrix)

print("\n--- Phase 3 Mock Integration ---")
print("Locations:", [l["address"].split(",")[0] for l in locations])
print("Raw route cost:", cost)
print("2-opt route:", [s.split(",")[0] for s in improved])
print("2-opt cost:", round(improved_cost, 1), "km")