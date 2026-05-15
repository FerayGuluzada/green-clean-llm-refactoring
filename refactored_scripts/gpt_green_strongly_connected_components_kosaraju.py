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

    def kosaraju(self, V, adj):
        visited = [False] * V
        order = []

        # Iterative DFS to avoid recursion overhead and reduce call-stack usage.
        for start in range(V):
            if visited[start]:
                continue

            stack = [(start, 0)]
            visited[start] = True

            while stack:
                node, idx = stack[-1]
                neighbors = adj[node]

                if idx < len(neighbors):
                    nxt = neighbors[idx]
                    stack[-1] = (node, idx + 1)
                    if not visited[nxt]:
                        visited[nxt] = True
                        stack.append((nxt, 0))
                else:
                    order.append(node)
                    stack.pop()

        adj1 = [[] for _ in range(V)]
        for u in range(V):
            for v in adj[u]:
                adj1[v].append(u)

        visited = [False] * V
        ans = 0

        for start in reversed(order):
            if visited[start]:
                continue

            ans += 1
            stack = [start]
            visited[start] = True

            while stack:
                node = stack.pop()
                for nxt in adj1[node]:
                    if not visited[nxt]:
                        visited[nxt] = True
                        stack.append(nxt)

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