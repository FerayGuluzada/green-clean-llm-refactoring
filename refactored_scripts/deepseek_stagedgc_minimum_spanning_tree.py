class Edge:
    __slots__ = ('u', 'v', 'weight')
    
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight


class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def merge(self, a, b):
        """Merge sets containing nodes a and b."""
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a
        
        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        return True

    def find(self, node):
        """Find root of node with path compression."""
        parent = self.parent
        
        # Find root
        root = node
        while parent[root] != root:
            root = parent[root]
        
        # Path compression
        while parent[node] != root:
            node, parent[node] = parent[node], root
        
        return root


def kruskal_mst_weight(n, edges):
    """
    Calculate total weight of Minimum Spanning Tree using Kruskal's algorithm.
    
    Args:
        n: Number of vertices
        edges: List of Edge objects
        
    Returns:
        Total weight of MST
    """
    edges.sort(key=lambda e: e.weight)
    ds = DisjointSet(n)
    mst_weight = 0
    edges_needed = n - 1
    
    for edge in edges:
        if ds.find(edge.u) != ds.find(edge.v):
            ds.merge(edge.u, edge.v)
            mst_weight += edge.weight
            edges_needed -= 1
            
            if edges_needed == 0:
                break
    
    return mst_weight


if __name__ == "__main__":
    # Test case 1
    n = 5
    edges = [
        Edge(0, 1, 3),
        Edge(0, 2, 8),
        Edge(1, 3, 5),
        Edge(2, 3, 2),
        Edge(2, 4, 4),
        Edge(3, 4, 6)
    ]
    
    print("MST weights sum:", kruskal_mst_weight(n, edges))  # Expected: 14