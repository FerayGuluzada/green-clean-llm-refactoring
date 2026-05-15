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

    def _dfs_fill_order(self, start_node, adj, visited, stack):
        dfs_stack = [(start_node, False)]

        while dfs_stack:
            node, expanded = dfs_stack.pop()

            if expanded:
                stack.append(node)
                continue

            if visited[node]:
                continue

            visited[node] = True
            dfs_stack.append((node, True))

            neighbors = adj[node]
            for i in range(len(neighbors) - 1, -1, -1):
                neighbor = neighbors[i]
                if not visited[neighbor]:
                    dfs_stack.append((neighbor, False))

    def _dfs_mark_component(self, start_node, adj, visited):
        dfs_stack = [start_node]
        visited[start_node] = True

        while dfs_stack:
            node = dfs_stack.pop()
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    dfs_stack.append(neighbor)

    def _transpose_graph(self, V, adj):
        transposed = [[] for _ in range(V)]
        for node, neighbors in enumerate(adj):
            for neighbor in neighbors:
                transposed[neighbor].append(node)
        return transposed

    def kosaraju(self, V, adj):
        stack = []
        visited = [False] * V
        dfs_fill_order = self._dfs_fill_order

        for node in range(V):
            if not visited[node]:
                dfs_fill_order(node, adj, visited, stack)

        transposed_adj = self._transpose_graph(V, adj)
        visited = [False] * V
        strongly_connected_components = 0
        dfs_mark_component = self._dfs_mark_component

        while stack:
            node = stack.pop()
            if not visited[node]:
                strongly_connected_components += 1
                dfs_mark_component(node, transposed_adj, visited)

        return strongly_connected_components


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