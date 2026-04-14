import heapq
from algorithms.graph import Graph 

def dijkstra(graph: Graph, source: str) -> tuple[dict, dict]:
    """
    Compute shortest paths from `source` to all reachable nodes.

    Returns:
        distances  — {node: minimum_cost}
        predecessors — {node: previous_node_on_shortest_path}
    """

    distances = {node: float("inf") for node in graph.get_all_nodes()}
    distances[source] = 0

    predecessors = {node: None for node in graph.get_all_nodes()}

    # Min-heap: (cost, node)
    heap = [(0, source)]
    visited = set()

    while heap:
        current_cost, current_node = heapq.heappop(heap)

        if current_node in visited:
            continue                   # stale entry — skip
        visited.add(current_node)

        for neighbor, weight in graph.get_neighbors(current_node):
            if neighbor in visited:
                continue

            new_cost = current_cost + weight
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                predecessors[neighbor] = current_node
                heapq.heappush(heap, (new_cost, neighbor))

    return distances, predecessors


def reconstruct_path(predecessors: dict, source: str, target: str) -> list[str]:
    """
    Walk backwards through predecessors to rebuild the full route.
    Returns an ordered list of nodes from source → target.
    """
    path = []
    node = target

    while node is not None:
        path.append(node)
        node = predecessors[node]

    path.reverse()

    # If path doesn't start at source, target is unreachable
    if path[0] != source:
        return []

    return path