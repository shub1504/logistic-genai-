from collections import defaultdict

class Graph:
    """
    Weighted directed graph for representing delivery locations
    and distances/travel-times between them.
    """

    def __init__(self):
        # adjacency list: {node: [(neighbor, weight), ...]}
        self.adjacency = defaultdict(list)
        self.nodes = set()

    def add_node(self, location: str):
        """Register a location (even if it has no edges yet)."""
        self.nodes.add(location)

    def add_edge(self, origin: str, destination: str, weight: float):
        """
        Add a directed edge from origin → destination with a
        given weight (distance in km, or travel time in minutes).
        """
        self.nodes.add(origin)
        self.nodes.add(destination)
        self.adjacency[origin].append((destination, weight))

    def add_undirected_edge(self, a: str, b: str, weight: float):
        """Convenience: add edges in both directions."""
        self.add_edge(a, b, weight)
        self.add_edge(b, a, weight)

    def get_neighbors(self, node: str) -> list[tuple[str, float]]:
        """Return [(neighbor, weight), ...] for a given node."""
        return self.adjacency.get(node, [])

    def get_all_nodes(self) -> set:
        return self.nodes

    def __repr__(self):
        lines = []
        for node in sorted(self.nodes):
            neighbors = self.adjacency.get(node, [])
            lines.append(f"  {node} → {neighbors}")
        return "Graph(\n" + "\n".join(lines) + "\n)"

__all__ = ["Graph"]