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

    def _dfs(self, vertex, visited, adj, stack):
        """Perform DFS traversal from vertex."""
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                self._dfs(neighbor, visited, adj, stack)
        stack.append(vertex)

    def _transpose_graph(self, vertices, adj):
        """Transpose the graph."""
        transposed_adj = [[] for _ in range(vertices)]
        for vertex in range(vertices):
            for neighbor in adj[vertex]:
                transposed_adj[neighbor].append(vertex)
        return transposed_adj

    def _count_strongly_connected_components(self, vertices, transposed_adj):
        """Count strongly connected components in the transposed graph."""
        visited = [False] * vertices
        count = 0
        for vertex in range(vertices):
            if not visited[vertex]:
                self._dfs(vertex, visited, transposed_adj, [])
                count += 1
        return count

    def kosaraju(self, vertices, adj):
        """
        Calculate the number of strongly connected components in a directed graph.

        Args:
            vertices (int): Number of vertices in the graph.
            adj (list): Adjacency list representation of the graph.

        Returns:
            int: Number of strongly connected components.
        """
        stack = []
        visited = [False] * vertices
        for vertex in range(vertices):
            if not visited[vertex]:
                self._dfs(vertex, visited, adj, stack)
        transposed_adj = self._transpose_graph(vertices, adj)
        return self._count_strongly_connected_components(vertices, transposed_adj)


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

    vertices, edges = 6, 7
    edges_list = [
        (0, 2),
        (1, 0),
        (2, 3),
        (3, 1),
        (3, 4),
        (4, 5),
        (5, 4)
    ]

    adj = [[] for _ in range(vertices)]
    for u, v in edges_list:
        adj[u].append(v)

    print(Kosaraju().kosaraju(vertices, adj))


if __name__ == '__main__':
    main()