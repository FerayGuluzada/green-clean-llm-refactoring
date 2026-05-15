class Edge:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight


class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))  # Each node is its own parent initially
        self.size = [1] * n           # Size of each set starts at 1

    def mergeSet(self, a, b):
        # Find roots and merge smaller set into larger set
        root_a = self.findSet(a)
        root_b = self.findSet(b)
        
        if root_a == root_b:
            return  # Already in same set
            
        # Union by size: attach smaller tree under root of larger tree
        if self.size[root_a] < self.size[root_b]:
            self.parent[root_a] = root_b
            self.size[root_b] += self.size[root_a]
        else:
            self.parent[root_b] = root_a
            self.size[root_a] += self.size[root_b]

    def findSet(self, a):
        # Path compression: make every node point directly to root
        if self.parent[a] != a:
            self.parent[a] = self.findSet(self.parent[a])
        return self.parent[a]


def kruskal(n, edges, ds):
    # Sort edges by weight
    edges.sort(key=lambda edge: edge.weight)
    
    mst_weight = 0
    edges_added = 0
    
    for edge in edges:
        # Check if nodes belong to different sets
        if ds.findSet(edge.u) != ds.findSet(edge.v):
            ds.mergeSet(edge.u, edge.v)
            mst_weight += edge.weight
            edges_added += 1
            
            # Early termination: MST complete with n-1 edges
            if edges_added == n - 1:
                break
                
    return mst_weight


if __name__ == "__main__":
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

    print("MST weights sum:", kruskal(n, edges, ds))  # Expected: 14