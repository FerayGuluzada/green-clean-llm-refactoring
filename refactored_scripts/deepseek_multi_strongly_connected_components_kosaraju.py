"""
Implementing strongly connected components in a graph using Kosaraju's algorithm.
https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
"""


class Kosaraju:
    """
    Kosaraju's algorithm use depth first search approach to find strongly connected components in a directed graph.
    Approach:
        1. Make a DFS call to keep track of finish time of each vertex.
        2. Transpose the original graph. ie 1->2 transpose is 1<-2
        3. Make another DFS call to calculate strongly connected components.
    """

    def _dfs(self, vertex, adj, visited, stack=None):
        """Depth-first search that optionally builds finish-time stack."""
        visited[vertex] = True
        
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                self._dfs(neighbor, adj, visited, stack)
        
        if stack is not None:
            stack.append(vertex)

    def _transpose_graph(self, V, adj):
        """Create transpose of adjacency list representation."""
        transposed = [[] for _ in range(V)]
        for src in range(V):
            for dest in adj[src]:
                transposed[dest].append(src)
        return transposed

    def kosaraju(self, V, adj):
        """Find number of strongly connected components."""
        # First DFS: build finish-time order
        visited = [False] * V
        finish_stack = []
        
        for vertex in range(V):
            if not visited[vertex]:
                self._dfs(vertex, adj, visited, finish_stack)
        
        # Second DFS on transposed graph
        transposed = self._transpose_graph(V, adj)
        visited = [False] * V
        scc_count = 0
        
        for vertex in reversed(finish_stack):
            if not visited[vertex]:
                scc_count += 1
                self._dfs(vertex, transposed, visited)
        
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