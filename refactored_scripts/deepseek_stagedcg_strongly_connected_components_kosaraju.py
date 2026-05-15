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

    def _dfs_iterative(self, start_vertex, adj, visited, stack):
        """Iterative DFS to avoid recursion overhead and push vertices to stack in post-order."""
        dfs_stack = [(start_vertex, 0)]  # (vertex, neighbor_index)
        visited[start_vertex] = True
        
        while dfs_stack:
            vertex, idx = dfs_stack[-1]
            
            if idx < len(adj[vertex]):
                neighbor = adj[vertex][idx]
                dfs_stack[-1] = (vertex, idx + 1)
                if not visited[neighbor]:
                    visited[neighbor] = True
                    dfs_stack.append((neighbor, 0))
            else:
                dfs_stack.pop()
                stack.append(vertex)

    def _transpose_graph(self, adj):
        """Return transposed adjacency list using pre-allocated list."""
        V = len(adj)
        transposed = [[] for _ in range(V)]
        
        # Pre-calculate neighbor counts to avoid repeated len() calls
        for src in range(V):
            neighbors = adj[src]
            for dest in neighbors:
                transposed[dest].append(src)
        return transposed

    def kosaraju(self, V, adj):
        # First DFS pass: fill stack with vertices in order of finish times
        visited = [False] * V
        stack = []
        
        for vertex in range(V):
            if not visited[vertex]:
                self._dfs_iterative(vertex, adj, visited, stack)

        # Transpose the graph
        transposed_adj = self._transpose_graph(adj)

        # Second DFS pass on transposed graph in reverse finish order
        visited = [False] * V
        scc_count = 0
        
        # Process stack in reverse without popping (use index)
        for i in range(len(stack) - 1, -1, -1):
            vertex = stack[i]
            if not visited[vertex]:
                scc_count += 1
                # Use iterative DFS for second pass as well
                self._dfs_iterative(vertex, transposed_adj, visited, [])
        
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