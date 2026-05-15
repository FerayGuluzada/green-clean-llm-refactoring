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

    def _dfs_finish_order(self, i, adj, visited, stk):
        """DFS to determine finish order of vertices."""
        visited[i] = True

        for neighbor in adj[i]:
            if not visited[neighbor]:
                self._dfs_finish_order(neighbor, adj, visited, stk)

        stk.append(i)

    def _dfs_count_components(self, i, adj, visited):
        """DFS to count vertices in a strongly connected component."""
        stack = [i]
        visited[i] = True
        
        while stack:
            current = stack.pop()
            for neighbor in adj[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)

    def kosaraju(self, V, adj):
        # First DFS to get finish order
        stk = []
        visited = [False] * V

        for i in range(V):
            if not visited[i]:
                self._dfs_finish_order(i, adj, visited, stk)

        # Transpose graph
        transposed_adj = [[] for _ in range(V)]
        for i in range(V):
            for neighbor in adj[i]:
                transposed_adj[neighbor].append(i)

        # Second DFS on transposed graph in reverse finish order
        visited = [False] * V
        component_count = 0

        while stk:
            node = stk.pop()
            if not visited[node]:
                component_count += 1
                self._dfs_count_components(node, transposed_adj, visited)

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