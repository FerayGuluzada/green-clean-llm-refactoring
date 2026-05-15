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

        self.parent = list(range(n))  # Contains which node is the parent of the node at position <i>
        self.size = [1] * n  # Contains size of node at index <i>, used to optimize merge

    def merge_set(self, a, b):
        # Args:
        #   a, b (int): Indexes of nodes whose sets will be merged.

        # Get the set of nodes at position <a> and <b>
        # If <a> and <b> are the roots, this will be constant O(1)
        a = self.find_set(a)
        b = self.find_set(b)

        # Join the shortest node to the longest, minimizing tree size (faster find)
        if self.size[a] < self.size[b]:
            self.parent[a] = b  # Merge set(a) and set(b)
            self.size[b] += self.size[a]  # Add size of old set(a) to set(b)
        else:
            self.parent[b] = a  # Merge set(b) and set(a)
            self.size[a] += self.size[b]  # Add size of old set(b) to set(a)

    def find_set(self, a):
        if self.parent[a]!= a: 
            # Very important, memoize result of the 
            # recursion in the list to optimize next
            # calls and make this operation practically constant, O(1)
            self.parent[a] = self.find_set(self.parent[a])

        # node <a> it's the set root, so we can return that index
        return self.parent[a]


def kruskal(n, edges, ds):
    # Args:
    #   n (int): Number of vertices in the graph
    #   edges (list of Edge): Edges of the graph
    #   ds (DisjointSet): DisjointSet of the vertices
    # Returns:
    #   int: sum of weights of the minimum spanning tree 

    # Sort the edges (criteria: less weight)
    edges.sort(key=lambda edge: edge.weight)

    mst_weight = 0
    mst_edges = 0

    for edge in edges:
        set_u = ds.find_set(edge.u)  # Set of the node <u>
        set_v = ds.find_set(edge.v)  # Set of the node <v>
        if set_u!= set_v:
            ds.merge_set(set_u, set_v)
            mst_weight += edge.weight
            mst_edges += 1
            if mst_edges == n - 1: 
                # If we have selected n-1 edges, all the other 
                # edges will be discarded, so, we can stop here
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