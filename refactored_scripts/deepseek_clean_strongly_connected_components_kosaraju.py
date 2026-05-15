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

    def _dfs(self, vertex, adj, visited, stack):
        """Perform DFS and push vertices to stack in post-order."""
        visited[vertex] = True
        
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                self._dfs(neighbor, adj, visited, stack)
        
        stack.append(vertex)

    def _transpose_graph(self, adj):
        """Return transpose of adjacency list graph."""
        transposed = [[] for _ in range(len(adj))]
        
        for src, neighbors in enumerate(adj):
            for dest in neighbors:
                transposed[dest].append(src)
        
        return transposed

    def kosaraju(self, V, adj):
        """Return number of strongly connected components."""
        visited = [False] * V
        order_stack = []
        
        # First DFS pass to get finishing order
        for vertex in range(V):
            if not visited[vertex]:
                self._dfs(vertex, adj, visited, order_stack)
        
        # Transpose graph
        transposed_adj = self._transpose_graph(adj)
        
        # Second DFS pass on transposed graph in reverse order
        visited = [False] * V
        scc_count = 0
        
        for vertex in reversed(order_stack):
            if not visited[vertex]:
                scc_count += 1
                self._dfs(vertex, transposed_adj, visited, [])
        
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