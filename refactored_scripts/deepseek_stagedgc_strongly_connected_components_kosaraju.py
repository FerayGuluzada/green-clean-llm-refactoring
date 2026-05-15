"""
Implementing strongly connected components in a graph using Kosaraju's algorithm.
https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
"""


class Kosaraju:
    """
    Kosaraju's algorithm uses depth-first search to find strongly connected components.
    Steps:
        1. First DFS: record finishing order of vertices
        2. Transpose the graph (reverse all edges)
        3. Second DFS: process vertices in reverse finishing order to find SCCs
    """

    def _dfs_fill_order(self, vertex, adj, visited, order_stack):
        """DFS that pushes vertices to stack after visiting all descendants."""
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                self._dfs_fill_order(neighbor, adj, visited, order_stack)
        order_stack.append(vertex)

    def _dfs_mark_component(self, vertex, adj, visited):
        """DFS that marks all vertices reachable from given vertex."""
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                self._dfs_mark_component(neighbor, adj, visited)

    def _transpose_graph(self, V, adj):
        """Return transpose (reverse) of the original graph."""
        transposed = [[] for _ in range(V)]
        for src in range(V):
            for dest in adj[src]:
                transposed[dest].append(src)
        return transposed

    def kosaraju(self, V, adj):
        # First DFS: compute finishing order
        visited = [False] * V
        order_stack = []
        for vertex in range(V):
            if not visited[vertex]:
                self._dfs_fill_order(vertex, adj, visited, order_stack)

        # Transpose the graph
        transposed_adj = self._transpose_graph(V, adj)

        # Second DFS: count SCCs using reversed order
        visited = [False] * V
        scc_count = 0
        for vertex in reversed(order_stack):
            if not visited[vertex]:
                scc_count += 1
                self._dfs_mark_component(vertex, transposed_adj, visited)
        return scc_count


def main():
    """
    Sample input:
    6 7  # vertices, edges
    0 2  # directed edge 0->2
    1 0
    2 3
    3 1
    3 4
    4 5
    5 4

    Expected number of strongly connected components: 2
    Component 1: 0->2->3->1->0
    Component 2: 4->5->4
    """
    V, E = 6, 7
    edges = [
        (0, 2),
        (1, 0),
        (2, 3),
        (3, 1),
        (3, 4),
        (4, 5),
        (5, 4)
    ]

    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)

    print(Kosaraju().kosaraju(V, adj))


if __name__ == '__main__':
    main()