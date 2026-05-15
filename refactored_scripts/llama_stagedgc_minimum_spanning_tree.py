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

    def _find_set(self, a):
        """Find the set of a node and apply path compression."""
        if self.parent[a]!= a:
            self.parent[a] = self._find_set(self.parent[a])
        return self.parent[a]

    def merge_sets(self, a, b):
        """Merge two sets."""
        a_root = self._find_set(a)
        b_root = self._find_set(b)

        if a_root!= b_root:
            if self.size[a_root] < self.size[b_root]:
                self.parent[a_root] = b_root
                self.size[b_root] += self.size[a_root]
            else:
                self.parent[b_root] = a_root
                self.size[a_root] += self.size[b_root]


def kruskal(n, edges, disjoint_set):
    """Kruskal algorithm to find the minimum spanning tree."""
    edges.sort(key=lambda edge: edge.weight)

    mst_weight = 0
    mst_edges = 0

    for edge in edges:
        if disjoint_set._find_set(edge.u)!= disjoint_set._find_set(edge.v):
            disjoint_set.merge_sets(edge.u, edge.v)
            mst_weight += edge.weight
            mst_edges += 1
            if mst_edges == n - 1:
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

    disjoint_set = DisjointSet(n)
    edges = [
        Edge(0, 1, 3),
        Edge(0, 2, 8),
        Edge(1, 3, 5),
        Edge(2, 3, 2),
        Edge(2, 4, 4),
        Edge(3, 4, 6),
    ]

    # After finish input and graph creation, use Kruskal algorithm for MST:
    print("MST weights sum:", kruskal(n, edges, disjoint_set))  # Expected: 14