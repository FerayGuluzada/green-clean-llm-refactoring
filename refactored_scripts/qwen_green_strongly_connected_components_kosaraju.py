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

    def dfs(self, i, adj, visited, stk):
        visited[i] = 1

        for x in adj[i]:
            if visited[x] == -1:
                self.dfs(x, adj, visited, stk)

        stk.append(i)

    def kosaraju(self, V, adj):
        # First DFS to get finish order
        stk = []
        visited = [-1] * V  # Removed unnecessary +1 size

        for i in range(V):
            if visited[i] == -1:
                self.dfs(i, adj, visited, stk)

        # Transpose graph
        adj1 = [[] for _ in range(V)]
        for i in range(V):
            for x in adj[i]:
                adj1[x].append(i)

        # Second DFS on transposed graph in reverse finish order
        visited1 = [-1] * V  # Removed unnecessary +1 size
        ans = 0

        while stk:
            node = stk.pop()  # Use stack directly instead of reversing
            if visited1[node] == -1:
                ans += 1
                # DFS without collecting stack (not needed for count)
                stack_dfs = [node]
                while stack_dfs:
                    current = stack_dfs.pop()
                    if visited1[current] == -1:
                        visited1[current] = 1
                        for neighbor in adj1[current]:
                            if visited1[neighbor] == -1:
                                stack_dfs.append(neighbor)

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