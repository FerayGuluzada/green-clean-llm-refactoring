# Minimum spanning tree (MST) is going to use an undirected graph
#
# The disjoint set is represented with an list <n> of integers where 
# <n[i]> is the parent of the node at position <i>.
# If <n[i]> = <i>, <i> it's a root, or a head, of a set


class Edge:
    __slots__ = ('u', 'v', 'weight')  # Reduces memory overhead and improves cache locality
    
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight


class DisjointSet:
    def __init__(self, n):
        # Args:
        #   n (int): Number of vertices in the graph
        self.parent = list(range(n))
        self.size = [1] * n

    def merge(self, a, b):
        # Args:
        #   a, b (int): Indexes of nodes whose sets will be merged.
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False  # Return status to avoid unnecessary work in caller

        # Union by size
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        return True

    def find(self, a):
        # Path compression with iterative approach (faster than recursion)
        root = a
        while self.parent[root] != root:
            root = self.parent[root]
        
        # Path compression
        while self.parent[a] != root:
            parent = self.parent[a]
            self.parent[a] = root
            a = parent
            
        return root


def kruskal(n, edges, ds):
    # Args:
    #   n (int): Number of vertices in the graph
    #   edges (list of Edge): Edges of the graph
    #   ds (DisjointSet): DisjointSet of the vertices
    # Returns:
    #   int: sum of weights of the minimum spanning tree 
    #
    # Kruskal algorithm:
    #   This algorithm will find the optimal graph with less edges and less
    #   total weight to connect all vertices (MST), the MST will always contain
    #   n-1 edges because it's the minimum required to connect n vertices.
    #
    # Procedure:
    #   Sort the edges (criteria: less weight).
    #   Only take edges of nodes in different sets.
    #   If we take a edge, we need to merge the sets to discard these.
    #   After repeat this until select n-1 edges, we will have the complete MST.
    
    # Early exit for trivial cases
    if n <= 1:
        return 0
    
    # Sort edges once - use built-in sort which is highly optimized
    edges.sort(key=lambda edge: edge.weight)
    
    mst_weight = 0
    edges_needed = n - 1
    
    # Pre-allocate loop variables for speed
    find = ds.find
    merge = ds.merge
    
    for edge in edges:
        if find(edge.u) != find(edge.v):
            if merge(edge.u, edge.v):
                mst_weight += edge.weight
                edges_needed -= 1
                
                if edges_needed == 0:
                    break

    return mst_weight


if __name__ == "__main__":
    # Test. How input works:
    # Input consists of different weighted, connected, undirected graphs. 
    # line 1: 
    #   integers n, m
    # lines 2..m+2:
    #   edge with the format -> node index u, node index v, integer weight
    #
    # Samples of input:
    #
    # 5 6
    # 1 2 3
    # 1 3 8
    # 2 4 5
    # 3 4 2
    # 3 5 4
    # 4 5 6
    # 
    # 3 3
    # 2 1 20
    # 3 1 20
    # 2 3 100
    #
    # Sum of weights of the optimal paths:
    # 14, 40

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

    # After finish input and graph creation, use Kruskal algorithm for MST:
    print("MST weights sum:", kruskal(n, edges, ds))  # Expected: 14