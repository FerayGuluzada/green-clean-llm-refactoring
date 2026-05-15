# Minimum spanning tree (MST) implementation using Kruskal's algorithm
# Uses an undirected graph and disjoint set data structure for efficiency

class Edge:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight

class DisjointSet:
    def __init__(self, n):
        """
        Initialize disjoint set structure.
        
        Args:
            n (int): Number of vertices in the graph
        """
        self.parent = list(range(n))  # Each node is its own parent initially
        self.size = [1] * n  # Size of each set for union by size optimization

    def mergeSet(self, a, b):
        """
        Merge two sets by size, attaching smaller tree to larger tree.
        
        Args:
            a, b (int): Indexes of nodes whose sets will be merged
        """
        if a == b:  # Already in the same set
            return
            
        # Join the smaller set to the larger one to minimize tree height
        if self.size[a] < self.size[b]:
            self.parent[a] = b
            self.size[b] += self.size[a]
        else:
            self.parent[b] = a
            self.size[a] += self.size[b]

    def findSet(self, a):
        """
        Find root of set with path compression optimization.
        
        Args:
            a (int): Node index
            
        Returns:
            int: Root of the set containing node a
        """
        if self.parent[a] != a:
            self.parent[a] = self.findSet(self.parent[a])  # Path compression
        return self.parent[a]

def kruskal(n, edges, ds):
    """
    Find minimum spanning tree weight using Kruskal's algorithm.
    
    Args:
        n (int): Number of vertices in the graph
        edges (list of Edge): Edges of the graph
        ds (DisjointSet): DisjointSet of the vertices
        
    Returns:
        int: Sum of weights of the minimum spanning tree
        
    Kruskal's algorithm:
        - Sort edges by weight
        - Add edges that connect different components
        - Stop when n-1 edges are added (MST complete)
    """
    # Sort edges by weight
    edges.sort(key=lambda edge: edge.weight)

    total_weight = 0
    edges_added = 0

    for edge in edges:
        set_u = ds.findSet(edge.u)
        set_v = ds.findSet(edge.v)
        
        # Only add edge if it connects two different components
        if set_u != set_v:
            ds.mergeSet(set_u, set_v)
            total_weight += edge.weight
            edges_added += 1
            
            # Early exit when MST is complete (n-1 edges)
            if edges_added == n - 1:
                break

    return total_weight

if __name__ == "__main__":
    # Test case: 5 vertices, 6 edges
    n = 5
    m = 6

    ds = DisjointSet(n)
    edges = [
        Edge(0, 1, 3),
        Edge(0, 2, 8),
        Edge(1, 3, 5),
        Edge(2, 3, 2),
        Edge(2, 4, 4),
        Edge(3, 4, 6)
    ]

    # Compute and print MST weight sum
    print("MST weights sum:", kruskal(n, edges, ds))  # Expected: 14