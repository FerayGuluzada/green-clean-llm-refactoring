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


def _build_neighbors(capacity):
    vertices = len(capacity)
    neighbors = [[] for _ in range(vertices)]
    for i, row_i in enumerate(capacity):
        neigh_i = neighbors[i]
        for j in range(vertices):
            if row_i[j] > 0 or capacity[j][i] > 0:
                neigh_i.append(j)
    return neighbors


def _augment_path(flow, parent, source, sink, amount):
    idx = sink
    while idx != source:
        prev = parent[idx]
        flow[prev][idx] += amount
        flow[idx][prev] -= amount
        idx = prev


def _find_path_flow(capacity, flow, parent, source, sink):
    amount = INF
    idx = sink
    while idx != source:
        prev = parent[idx]
        residual = capacity[prev][idx] - flow[prev][idx]
        if residual < amount:
            amount = residual
        idx = prev
    return amount


def dfs(capacity, flow, visit, neighbors, idx, sink, current_flow=INF):
    # DFS function for ford_fulkerson algorithm.
    if idx == sink:
        return current_flow

    visit[idx] = True
    flow_idx = flow[idx]
    cap_idx = capacity[idx]

    for nxt in neighbors[idx]:
        residual = cap_idx[nxt] - flow_idx[nxt]
        if visit[nxt] or residual <= 0:
            continue
        pushed = dfs(capacity, flow, visit, neighbors, nxt, sink, min(current_flow, residual))
        if pushed:
            flow_idx[nxt] += pushed
            flow[nxt][idx] -= pushed
            return pushed
    return 0


def ford_fulkerson(capacity, source, sink):
    # Computes maximum flow from source to sink using DFS.
    # Time Complexity : O(Ef)
    # E is the number of edges and f is the maximum flow in the graph.
    vertices = len(capacity)
    neighbors = _build_neighbors(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0

    while True:
        visit = [False] * vertices
        pushed = dfs(capacity, flow, visit, neighbors, source, sink)
        if not pushed:
            return max_flow
        max_flow += pushed


def edmonds_karp(capacity, source, sink):
    # Computes maximum flow from source to sink using BFS.
    # Time complexity : O(V*E^2)
    # V is the number of vertices and E is the number of edges.
    vertices = len(capacity)
    neighbors = _build_neighbors(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0

    while True:
        parent = [-1] * vertices
        parent[source] = source
        q = deque([source])

        # Finds new flow using BFS.
        while q and parent[sink] == -1:
            idx = q.popleft()
            flow_idx = flow[idx]
            cap_idx = capacity[idx]
            for nxt in neighbors[idx]:
                if parent[nxt] != -1 or cap_idx[nxt] - flow_idx[nxt] <= 0:
                    continue
                parent[nxt] = idx
                q.append(nxt)

        if parent[sink] == -1:
            return max_flow

        pushed = _find_path_flow(capacity, flow, parent, source, sink)
        max_flow += pushed
        _augment_path(flow, parent, source, sink, pushed)


def dinic_bfs(capacity, flow, level, neighbors, source, sink):
    # BFS function for Dinic algorithm.
    # Check whether sink is reachable only using edges that is not full.
    q = deque([source])
    level[source] = 0

    while q:
        idx = q.popleft()
        next_level = level[idx] + 1
        flow_idx = flow[idx]
        cap_idx = capacity[idx]
        for nxt in neighbors[idx]:
            if level[nxt] != -1 or cap_idx[nxt] - flow_idx[nxt] <= 0:
                continue
            level[nxt] = next_level
            if nxt == sink:
                return True
            q.append(nxt)
    return level[sink] != -1


def dinic_dfs(capacity, flow, level, neighbors, idx, sink, work, current_flow=INF):
    # DFS function for Dinic algorithm.
    # Finds new flow using edges that is not full.
    if idx == sink:
        return current_flow

    neigh = neighbors[idx]
    flow_idx = flow[idx]
    cap_idx = capacity[idx]

    while work[idx] < len(neigh):
        nxt = neigh[work[idx]]
        residual = cap_idx[nxt] - flow_idx[nxt]
        if level[nxt] == level[idx] + 1 and residual > 0:
            pushed = dinic_dfs(
                capacity,
                flow,
                level,
                neighbors,
                nxt,
                sink,
                work,
                min(current_flow, residual),
            )
            if pushed:
                flow_idx[nxt] += pushed
                flow[nxt][idx] -= pushed
                return pushed
        work[idx] += 1
    return 0


def dinic(capacity, source, sink):
    # Computes maximum flow from source to sink using Dinic algorithm.
    # Time complexity : O(V^2*E)
    # V is the number of vertices and E is the number of edges.
    vertices = len(capacity)
    neighbors = _build_neighbors(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0

    while True:
        level = [-1] * vertices
        if not dinic_bfs(capacity, flow, level, neighbors, source, sink):
            return max_flow

        work = [0] * vertices
        while True:
            pushed = dinic_dfs(capacity, flow, level, neighbors, source, sink, work)
            if not pushed:
                break
            max_flow += pushed


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