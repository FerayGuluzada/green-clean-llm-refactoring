class Edge:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight


class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))  # Each node is its own parent initially
        self.size = [1] * n  # Size of each set for union by size optimization

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        
        if root_a == root_b:
            return False  # Already in same set
            
        # Union by size: attach smaller tree to root of larger tree
        if self.size[root_a] < self.size[root_b]:
            self.parent[root_a] = root_b
            self.size[root_b] += self.size[root_a]
        else:
            self.parent[root_b] = root_a
            self.size[root_a] += self.size[root_b]
        return True

    def find(self, x):
        # Path compression: make every node point directly to root
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]


def kruskal(n, edges):
    # Sort edges by weight in ascending order
    edges.sort(key=lambda edge: edge.weight)
    
    ds = DisjointSet(n)
    mst_weight = 0
    edges_added = 0
    
    for edge in edges:
        # If nodes are in different sets, add edge to MST
        if ds.union(edge.u, edge.v):
            mst_weight += edge.weight
            edges_added += 1
            
            # MST complete when we have n-1 edges
            if edges_added == n - 1:
                break
                
    return mst_weight


if __name__ == "__main__":
    n = 5
    edges = [
        Edge(0, 1, 3),
        Edge(0, 2, 8),
        Edge(1, 3, 5),
        Edge(2, 3, 2),
        Edge(2, 4, 4),
        Edge(3, 4, 6)
    ]
    
    print("MST weights sum:", kruskal(n, edges))  # Expected: 14