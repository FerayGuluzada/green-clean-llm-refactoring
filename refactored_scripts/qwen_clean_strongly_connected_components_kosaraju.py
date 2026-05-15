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

    def dfs_finish_order(self, node, adj, visited, finish_stack):
        """Perform DFS and record vertices in order of their finish time."""
        visited[node] = True
        
        for neighbor in adj[node]:
            if not visited[neighbor]:
                self.dfs_finish_order(neighbor, adj, visited, finish_stack)
                
        finish_stack.append(node)

    def transpose_graph(self, V, adj):
        """Create transpose of the graph."""
        transposed = [[] for _ in range(V)]
        
        for vertex in range(V):
            for neighbor in adj[vertex]:
                transposed[neighbor].append(vertex)
                
        return transposed

    def dfs_count_components(self, node, adj, visited):
        """Perform DFS to count nodes in a component."""
        visited[node] = True
        
        for neighbor in adj[node]:
            if not visited[neighbor]:
                self.dfs_count_components(neighbor, adj, visited)

    def kosaraju(self, V, adj):
        # Step 1: Get finish order of vertices using DFS
        visited = [False] * V
        finish_stack = []
        
        for i in range(V):
            if not visited[i]:
                self.dfs_finish_order(i, adj, visited, finish_stack)
        
        # Step 2: Transpose the graph
        transposed_adj = self.transpose_graph(V, adj)
        
        # Step 3: Process vertices in reverse finish order to count SCCs
        visited = [False] * V
        scc_count = 0
        
        while finish_stack:
            node = finish_stack.pop()
            if not visited[node]:
                scc_count += 1
                self.dfs_count_components(node, transposed_adj, visited)
                
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