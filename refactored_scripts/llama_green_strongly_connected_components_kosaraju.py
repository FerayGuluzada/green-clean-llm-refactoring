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

    def dfs(self, i, V, adj, visited, stk):
        """Perform DFS traversal from vertex i."""
        visited[i] = 1

        # Iterate over adjacent vertices
        for x in adj[i]:
            if visited[x] == -1:
                self.dfs(x, V, adj, visited, stk)

        # Push vertex to stack after visiting all its adjacent vertices
        stk.append(i)

    def kosaraju(self, V, adj):
        """
        Calculate the number of strongly connected components in a directed graph.

        Args:
            V (int): Number of vertices in the graph.
            adj (list): Adjacency list representation of the graph.

        Returns:
            int: Number of strongly connected components.
        """

        # Initialize stack and visited array
        stk, visited = [], [-1] * (V)

        # Perform DFS traversal to fill the stack with vertices in the order of their finish times
        for i in range(V):
            if visited[i] == -1:
                self.dfs(i, V, adj, visited, stk)

        # Reverse the stack to get the order of vertices for the second DFS traversal
        stk.reverse()

        # Initialize variables for the second DFS traversal
        ans, visited1 = 0, [-1] * (V)
        adj1 = [[] for _ in range(V)]

        # Transpose the graph
        for i in range(V):
            for x in adj[i]:
                adj1[x].append(i)

        # Perform the second DFS traversal to calculate strongly connected components
        for i in stk:
            if visited1[i] == -1:
                ans += 1
                self.dfs(i, V, adj1, visited1, [])

        return ans


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