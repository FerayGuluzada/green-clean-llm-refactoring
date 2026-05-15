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

    @staticmethod
    def _build_transpose(V, adj):
        transpose = [[] for _ in range(V)]
        for u in range(V):
            for v in adj[u]:
                transpose[v].append(u)
        return transpose

    @staticmethod
    def _fill_finish_order(V, adj):
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

        return order

    @staticmethod
    def _count_components(order, transpose, V):
        visited = [False] * V
        components = 0

        for start in reversed(order):
            if visited[start]:
                continue

            components += 1
            stack = [start]
            visited[start] = True

            while stack:
                node = stack.pop()
                for nxt in transpose[node]:
                    if not visited[nxt]:
                        visited[nxt] = True
                        stack.append(nxt)

        return components

    def kosaraju(self, V, adj):
        order = self._fill_finish_order(V, adj)
        transpose = self._build_transpose(V, adj)
        return self._count_components(order, transpose, V)


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