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

    def _dfs_finish_time(self, node, adj, visited, finish_stack):
        """DFS to determine finish times of vertices."""
        # Iterative DFS to avoid recursion overhead
        stack = [node]
        path = []
        
        while stack:
            current = stack.pop()
            if not visited[current]:
                visited[current] = True
                path.append(current)
                # Add sentinel to mark completion
                stack.append(-1)
                # Add neighbors in reverse order to maintain original traversal order
                for neighbor in reversed(adj[current]):
                    if not visited[neighbor]:
                        stack.append(neighbor)
            elif current == -1:  # Sentinel marker
                # Pop the completed node from path
                finish_stack.append(path.pop())
    
    def _transpose_graph(self, V, adj):
        """Create transpose of the graph."""
        transposed = [[] for _ in range(V)]
        
        for u in range(V):
            for v in adj[u]:
                transposed[v].append(u)
                
        return transposed

    def _dfs_strong_components(self, node, adj, visited):
        """DFS to count vertices in each strongly connected component."""
        # Iterative DFS to avoid recursion overhead
        stack = [node]
        component_size = 0
        
        while stack:
            current = stack.pop()
            if not visited[current]:
                visited[current] = True
                component_size += 1
                for neighbor in adj[current]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
        
        return component_size

    def kosaraju(self, V, adj):
        # Step 1: Get finish time order using DFS
        visited = [False] * V
        finish_stack = []
        
        for i in range(V):
            if not visited[i]:
                self._dfs_finish_time(i, adj, visited, finish_stack)
        
        # Step 2: Transpose the graph
        transposed_adj = self._transpose_graph(V, adj)
        
        # Step 3: DFS on transposed graph in order of finish times
        visited = [False] * V
        component_count = 0
        
        while finish_stack:
            node = finish_stack.pop()
            if not visited[node]:
                component_count += 1
                self._dfs_strong_components(node, transposed_adj, visited)
                
        return component_count


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