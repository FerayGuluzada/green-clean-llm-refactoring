"""
Implementing strongly connected components in a graph using Kosaraju's algorithm.
https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
"""


class Kosaraju:
    """
    Kosaraju's algorithm use depth first search approach to find strongly connected components in a directed graph.
    Approach:
        1. Make a DFS call to keep track of finish time of each vertex.
        2. Tranpose the original graph. ie 1->2 transpose is 1<-2
        3. Make another DFS call to calculate strongly connected components.
    """

    def _dfs_fill_order(self, node, adj, visited, order):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                self._dfs_fill_order(neighbor, adj, visited, order)
        order.append(node)

    def _dfs_mark_component(self, node, adj, visited):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                self._dfs_mark_component(neighbor, adj, visited)

    def _transpose_graph(self, V, adj):
        transposed = [[] for _ in range(V)]
        for node in range(V):
            for neighbor in adj[node]:
                transposed[neighbor].append(node)
        return transposed

    def kosaraju(self, V, adj):
        order = []
        visited = [False] * V

        for node in range(V):
            if not visited[node]:
                self._dfs_fill_order(node, adj, visited, order)

        transposed = self._transpose_graph(V, adj)
        visited = [False] * V
        scc_count = 0

        for node in reversed(order):
            if not visited[node]:
                scc_count += 1
                self._dfs_mark_component(node, transposed, visited)

        return scc_count


def main():
    """
    Let's look at the sample input.

    6 7  #no of vertex, no of edges
    0 2  #directed edge 0->2
    1 0
    2 3
    3 1
    3 4
    4 5
    5 4

    calculating no of strongly connected compnenets in a directed graph.
    answer should be: 2
    1st strong component: 0->2->3->1->0
    2nd strongly connected component: 4->5->4
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