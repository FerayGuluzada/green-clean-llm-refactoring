class Edge:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight


class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find_set(self, a):
        if self.parent[a] != a:
            self.parent[a] = self.find_set(self.parent[a])
        return self.parent[a]

    def merge_set(self, a, b):
        a_root = self.find_set(a)
        b_root = self.find_set(b)

        if a_root == b_root:
            return

        if self.size[a_root] < self.size[b_root]:
            a_root, b_root = b_root, a_root

        self.parent[b_root] = a_root
        self.size[a_root] += self.size[b_root]


def kruskal(n, edges, ds):
    edges.sort(key=lambda edge: edge.weight)
    mst_weight = 0
    edges_taken = 0

    for edge in edges:
        if ds.find_set(edge.u) != ds.find_set(edge.v):
            ds.merge_set(edge.u, edge.v)
            mst_weight += edge.weight
            edges_taken += 1
            if edges_taken == n - 1:
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

    print("MST weights sum:", kruskal(n, edges, ds))