"""
Given the capacity, source and sink of a graph,
computes the maximum flow from source to sink.
Input : capacity, source, sink
Output : maximum flow from source to sink
Capacity is a two-dimensional array that is v*v.
capacity[i][j] implies the capacity of the edge from i to j.
If there is no edge from i to j, capacity[i][j] should be zero.
"""

from collections import deque

INF = 1 << 63


def _create_flow_matrix(vertices):
    return [[0] * vertices for _ in range(vertices)]


def _build_neighbors(capacity):
    vertices = len(capacity)
    neighbors = [[] for _ in range(vertices)]

    for u in range(vertices):
        row = capacity[u]
        adj = neighbors[u]
        for v, cap in enumerate(row):
            if cap > 0:
                adj.append(v)
                neighbors[v].append(u)

    return [tuple(adj) for adj in neighbors]


def dfs(capacity, flow, neighbors, visit, idx, sink, current_flow=INF):
    # DFS function for ford_fulkerson algorithm.
    if idx == sink:
        return current_flow

    visit[idx] = True
    flow_row = flow[idx]
    capacity_row = capacity[idx]

    for nxt in neighbors[idx]:
        if visit[nxt]:
            continue

        residual = capacity_row[nxt] - flow_row[nxt]
        if residual <= 0:
            continue

        pushed = dfs(
            capacity,
            flow,
            neighbors,
            visit,
            nxt,
            sink,
            residual if residual < current_flow else current_flow,
        )
        if pushed:
            flow_row[nxt] += pushed
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
    neighbors = _build_neighbors(capacity)

    while True:
        visit = [False] * vertices
        pushed = dfs(capacity, flow, neighbors, visit, source, sink)
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
    neighbors = _build_neighbors(capacity)

    while True:
        q = deque([source])
        parent = [-1] * vertices
        path_flow = [0] * vertices

        parent[source] = source
        path_flow[source] = INF

        # Finds new flow using BFS.
        while q and parent[sink] == -1:
            idx = q.popleft()
            current_flow = path_flow[idx]
            flow_row = flow[idx]
            capacity_row = capacity[idx]

            for nxt in neighbors[idx]:
                if parent[nxt] != -1:
                    continue

                residual = capacity_row[nxt] - flow_row[nxt]
                if residual <= 0:
                    continue

                parent[nxt] = idx
                path_flow[nxt] = residual if residual < current_flow else current_flow
                if nxt == sink:
                    break
                q.append(nxt)

        if parent[sink] == -1:
            break

        pushed = path_flow[sink]
        max_flow += pushed

        idx = sink
        # Update flow array following parent starting from sink.
        while idx != source:
            prev = parent[idx]
            flow[prev][idx] += pushed
            flow[idx][prev] -= pushed
            idx = prev

    return max_flow


def dinic_bfs(capacity, flow, neighbors, level, source, sink):
    # BFS function for Dinic algorithm.
    # Check whether sink is reachable only using edges that is not full.
    q = deque([source])
    level[source] = 0

    while q:
        current = q.popleft()
        next_level = level[current] + 1
        flow_row = flow[current]
        capacity_row = capacity[current]

        for nxt in neighbors[current]:
            if level[nxt] != -1:
                continue
            if capacity_row[nxt] - flow_row[nxt] <= 0:
                continue

            level[nxt] = next_level
            if nxt == sink:
                return True
            q.append(nxt)

    return level[sink] != -1


def dinic_dfs(capacity, flow, neighbors, level, idx, sink, work, current_flow=INF):
    # DFS function for Dinic algorithm.
    # Finds new flow using edges that is not full.
    if idx == sink:
        return current_flow

    adj = neighbors[idx]
    flow_row = flow[idx]
    capacity_row = capacity[idx]

    while work[idx] < len(adj):
        nxt = adj[work[idx]]

        if level[nxt] == level[idx] + 1:
            residual = capacity_row[nxt] - flow_row[nxt]
            if residual > 0:
                pushed = dinic_dfs(
                    capacity,
                    flow,
                    neighbors,
                    level,
                    nxt,
                    sink,
                    work,
                    residual if residual < current_flow else current_flow,
                )
                if pushed > 0:
                    flow_row[nxt] += pushed
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
    neighbors = _build_neighbors(capacity)
    max_flow = 0

    while True:
        level = [-1] * vertices

        if not dinic_bfs(capacity, flow, neighbors, level, source, sink):
            break

        work = [0] * vertices
        while True:
            pushed = dinic_dfs(capacity, flow, neighbors, level, source, sink, work)
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