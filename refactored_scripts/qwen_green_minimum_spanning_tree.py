# Minimum spanning tree (MST) is going to use an undirected graph
#
# The disjoint set is represented with an list <n> of integers where 
# <n[i]> is the parent of the node at position <i>.
# If <n[i]> = <i>, <i> it's a root, or a head, of a set


class Edge:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight


class DisjointSet:
    def __init__(self, n):
        # Args:
        #   n (int): Number of vertices in the graph

        self.parent = list(range(n))  # Each node is its own parent initially
        self.size = [1] * n  # Size of each set for union by size optimization

    def mergeSet(self, a, b):
        # Args:
        #   a, b (int): Indexes of nodes whose sets will be merged.
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
        # Path compression: make all nodes point directly to root
        if self.parent[a] != a:
            self.parent[a] = self.findSet(self.parent[a])
        return self.parent[a]


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
    
    # Sort edges by weight
    edges.sort(key=lambda edge: edge.weight)

    total_weight = 0  # Accumulate weight directly instead of storing edges
    edges_added = 0   # Counter for early termination

    for edge in edges:
        set_u = ds.findSet(edge.u)
        set_v = ds.findSet(edge.v)
        
        if set_u != set_v:
            ds.mergeSet(set_u, set_v)
            total_weight += edge.weight
            edges_added += 1
            
            if edges_added == n - 1:  # Early exit when MST is complete
                break

    return total_weight


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
    edges = [None] * m

    edges[0] = Edge(0, 1, 3)
    edges[1] = Edge(0, 2, 8)
    edges[2] = Edge(1, 3, 5)
    edges[3] = Edge(2, 3, 2)
    edges[4] = Edge(2, 4, 4)
    edges[5] = Edge(3, 4, 6)

    # After finish input and graph creation, use Kruskal algorithm for MST:
    print("MST weights sum:", kruskal(n, edges, ds))  # Expected: 14