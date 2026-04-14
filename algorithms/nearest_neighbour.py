def nearest_neighbor_route(
    distance_matrix: dict[str, dict[str, float]],
    start: str,
    locations: list[str]
) -> tuple[list[str], float]:
    """
    Build a route visiting all `locations` using the nearest-neighbor
    heuristic, starting (and optionally returning) from `start`.

    Args:
        distance_matrix: {origin: {destination: cost}}
        start:           The depot or starting location
        locations:       All stops to visit (may or may not include start)

    Returns:
        route       — ordered list of locations
        total_cost  — sum of all edge weights along the route
    """

    unvisited = set(locations)
    unvisited.discard(start)   # don't revisit the start mid-route

    route = [start]
    total_cost = 0.0
    current = start

    while unvisited:
        # Find the nearest unvisited stop from current position
        nearest = min(
            unvisited,
            key=lambda loc: distance_matrix.get(current, {}).get(loc, float("inf"))
        )

        leg_cost = distance_matrix.get(current, {}).get(nearest, float("inf"))

        if leg_cost == float("inf"):
            # Can't reach this node — break to avoid an infinite loop
            print(f"Warning: no route from {current} to {nearest}")
            break

        route.append(nearest)
        total_cost += leg_cost
        unvisited.remove(nearest)
        current = nearest

    # Optional: return to start (depot round-trip)
    return_cost = distance_matrix.get(current, {}).get(start, 0.0)
    route.append(start)
    total_cost += return_cost

    return route, total_cost


def two_opt_improve(
    route: list[str],
    distance_matrix: dict[str, dict[str, float]],
    max_iterations: int = 100
) -> tuple[list[str], float]:
    """
    2-opt local search: try reversing every sub-segment of the route
    and keep improvements. Polishes the nearest-neighbor solution.

    Run this after nearest_neighbor_route for a noticeably better result.
    """

    def route_cost(r):
        return sum(
            distance_matrix.get(r[i], {}).get(r[i+1], float("inf"))
            for i in range(len(r) - 1)
        )

    best = route[:]
    improved = True
    iterations = 0

    while improved and iterations < max_iterations:
        improved = False
        iterations += 1

        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best) - 1):
                # Reverse the segment between i and j
                candidate = best[:i] + best[i:j+1][::-1] + best[j+1:]
                if route_cost(candidate) < route_cost(best):
                    best = candidate
                    improved = True

    return best, route_cost(best)