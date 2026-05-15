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

    def _dfs(self, vertex, visited, stack, adjacency_list):
        """Perform DFS traversal from a given vertex."""
        visited[vertex] = True
        for neighbor in adjacency_list[vertex]:
            if not visited[neighbor]:
                self._dfs(neighbor, visited, stack, adjacency_list)
        stack.append(vertex)

    def _transpose_graph(self, adjacency_list):
        """Transpose the given graph."""
        transposed_adjacency_list = [[] for _ in range(len(adjacency_list))]
        for vertex, neighbors in enumerate(adjacency_list):
            for neighbor in neighbors:
                transposed_adjacency_list[neighbor].append(vertex)
        return transposed_adjacency_list

    def kosaraju(self, num_vertices, adjacency_list):
        """Find strongly connected components in a directed graph using Kosaraju's algorithm."""
        stack = []
        visited = [False] * num_vertices

        # First DFS pass to fill the stack with vertices in the order of their finish times
        for vertex in range(num_vertices):
            if not visited[vertex]:
                self._dfs(vertex, visited, stack, adjacency_list)

        # Transpose the graph
        transposed_adjacency_list = self._transpose_graph(adjacency_list)

        # Reset visited array for the second DFS pass
        visited = [False] * num_vertices

        # Initialize count of strongly connected components
        strongly_connected_components = 0

        # Perform second DFS pass to find strongly connected components
        while stack:
            vertex = stack.pop()
            if not visited[vertex]:
                strongly_connected_components += 1
                self._dfs(vertex, visited, [], transposed_adjacency_list)

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

    num_vertices, num_edges = 6, 7
    edges = [
        (0, 2),
        (1, 0),
        (2, 3),
        (3, 1),
        (3, 4),
        (4, 5),
        (5, 4)
    ]

    adjacency_list = [[] for _ in range(num_vertices)]
    for u, v in edges:
        adjacency_list[u].append(v)

    print(Kosaraju().kosaraju(num_vertices, adjacency_list))

if __name__ == '__main__':
    main()