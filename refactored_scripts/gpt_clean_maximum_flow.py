"""
Given the capacity, source and sink of a graph,
computes the maximum flow from source to sink.
Input : capacity, source, sink
Output : maximum flow from source to sink
Capacity is a two-dimensional array that is v*v.
capacity[i][j] implies the capacity of the edge from i to j.
If there is no edge from i to j, capacity[i][j] should be zero.
"""

import queue

INF = 1 << 63


def _create_flow_matrix(vertices):
    return [[0] * vertices for _ in range(vertices)]


def _residual_capacity(capacity, flow, u, v):
    return capacity[u][v] - flow[u][v]


def dfs(capacity, flow, visit, vertices, idx, sink, current_flow=INF):
    # DFS function for ford_fulkerson algorithm.
    if idx == sink:
        return current_flow

    visit[idx] = True
    for nxt in range(vertices):
        residual = _residual_capacity(capacity, flow, idx, nxt)
        if visit[nxt] or residual <= 0:
            continue

        pushed = dfs(
            capacity,
            flow,
            visit,
            vertices,
            nxt,
            sink,
            min(current_flow, residual),
        )
        if pushed:
            flow[idx][nxt] += pushed
            flow[nxt][idx] -= pushed
            return pushed
    return 0


def ford_fulkerson(capacity, source, sink):
    # Computes maximum flow from source to sink using DFS.
    # Time Complexity : O(Ef)
    # E is the number of edges and f is the maximum flow in the graph.
    vertices = len(capacity)
    max_flow = 0
    flow = _create_flow_matrix(vertices)

    while True:
        visit = [False] * vertices
        pushed = dfs(capacity, flow, visit, vertices, source, sink)
        if not pushed:
            break
        max_flow += pushed

    return max_flow


def edmonds_karp(capacity, source, sink):
    # Computes maximum flow from source to sink using BFS.
    # Time complexity : O(V*E^2)
    # V is the number of vertices and E is the number of edges.
    vertices = len(capacity)
    max_flow = 0
    flow = _create_flow_matrix(vertices)

    while True:
        q = queue.Queue()
        visit = [False] * vertices
        parent = [-1] * vertices
        path_flow = [0] * vertices

        visit[source] = True
        path_flow[source] = INF
        q.put(source)

        # Finds new flow using BFS.
        while not q.empty():
            idx = q.get()
            if idx == sink:
                break

            current_flow = path_flow[idx]
            for nxt in range(vertices):
                residual = _residual_capacity(capacity, flow, idx, nxt)
                if visit[nxt] or residual <= 0:
                    continue

                visit[nxt] = True
                parent[nxt] = idx
                path_flow[nxt] = min(current_flow, residual)
                q.put(nxt)

        if parent[sink] == -1:
            break

        pushed = path_flow[sink]
        max_flow += pushed

        idx = sink
        # Update flow array following parent starting from sink.
        while parent[idx] != -1:
            prev = parent[idx]
            flow[prev][idx] += pushed
            flow[idx][prev] -= pushed
            idx = prev

    return max_flow


def dinic_bfs(capacity, flow, level, source, sink):
    # BFS function for Dinic algorithm.
    # Check whether sink is reachable only using edges that is not full.
    vertices = len(capacity)
    q = queue.Queue()
    q.put(source)
    level[source] = 0

    while not q.empty():
        current = q.get()
        for nxt in range(vertices):
            if level[nxt] != -1:
                continue
            if _residual_capacity(capacity, flow, current, nxt) <= 0:
                continue

            level[nxt] = level[current] + 1
            q.put(nxt)

    return level[sink] != -1


def dinic_dfs(capacity, flow, level, idx, sink, work, current_flow=INF):
    # DFS function for Dinic algorithm.
    # Finds new flow using edges that is not full.
    if idx == sink:
        return current_flow

    vertices = len(capacity)
    while work[idx] < vertices:
        nxt = work[idx]
        residual = _residual_capacity(capacity, flow, idx, nxt)

        if level[nxt] == level[idx] + 1 and residual > 0:
            pushed = dinic_dfs(
                capacity,
                flow,
                level,
                nxt,
                sink,
                work,
                min(current_flow, residual),
            )
            if pushed > 0:
                flow[idx][nxt] += pushed
                flow[nxt][idx] -= pushed
                return pushed

        work[idx] += 1

    return 0


def dinic(capacity, source, sink):
    # Computes maximum flow from source to sink using Dinic algorithm.
    # Time complexity : O(V^2*E)
    # V is the number of vertices and E is the number of edges.
    vertices = len(capacity)
    flow = _create_flow_matrix(vertices)
    max_flow = 0

    while True:
        level = [-1] * vertices
        work = [0] * vertices

        if not dinic_bfs(capacity, flow, level, source, sink):
            break

        while True:
            pushed = dinic_dfs(capacity, flow, level, source, sink, work)
            if pushed <= 0:
                break
            max_flow += pushed

    return max_flow


if __name__ == "__main__":
    capacity = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0],
    ]
    source = 0
    sink = 5

    print(ford_fulkerson(capacity, source, sink))
    print(edmonds_karp(capacity, source, sink))
    print(dinic(capacity, source, sink))