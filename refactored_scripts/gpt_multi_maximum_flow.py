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


def _init_flow(vertices):
    return [[0] * vertices for _ in range(vertices)]


def dfs(capacity, flow, visit, vertices, idx, sink, current_flow=INF):
    # DFS function for ford_fulkerson algorithm.
    if idx == sink:
        return current_flow

    visit[idx] = True
    cap_row = capacity[idx]
    flow_row = flow[idx]

    for nxt in range(vertices):
        residual = cap_row[nxt] - flow_row[nxt]
        if not visit[nxt] and residual > 0:
            pushed = dfs(capacity, flow, visit, vertices, nxt, sink, min(current_flow, residual))
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
    ret = 0
    flow = _init_flow(vertices)

    while True:
        visit = [False] * vertices
        pushed = dfs(capacity, flow, visit, vertices, source, sink)
        if not pushed:
            return ret
        ret += pushed


def edmonds_karp(capacity, source, sink):
    # Computes maximum flow from source to sink using BFS.
    # Time complexity : O(V*E^2)
    # V is the number of vertices and E is the number of edges.
    vertices = len(capacity)
    ret = 0
    flow = _init_flow(vertices)

    while True:
        par = [-1] * vertices
        par[source] = source
        path_flow = [0] * vertices
        path_flow[source] = INF
        q = deque([source])

        # Finds new flow using BFS.
        while q and par[sink] == -1:
            idx = q.popleft()
            cap_row = capacity[idx]
            flow_row = flow[idx]
            current_flow = path_flow[idx]

            for nxt in range(vertices):
                residual = cap_row[nxt] - flow_row[nxt]
                if par[nxt] == -1 and residual > 0:
                    par[nxt] = idx
                    path_flow[nxt] = min(current_flow, residual)
                    if nxt == sink:
                        break
                    q.append(nxt)

        if par[sink] == -1:
            return ret

        pushed = path_flow[sink]
        ret += pushed
        idx = sink

        # Update flow array following parent starting from sink.
        while idx != source:
            parent = par[idx]
            flow[parent][idx] += pushed
            flow[idx][parent] -= pushed
            idx = parent


def dinic_bfs(capacity, flow, level, source, sink):
    # BFS function for Dinic algorithm.
    # Check whether sink is reachable only using edges that is not full.
    vertices = len(capacity)
    q = deque([source])
    level[source] = 0

    while q:
        idx = q.popleft()
        cap_row = capacity[idx]
        flow_row = flow[idx]
        next_level = level[idx] + 1

        for nxt in range(vertices):
            if level[nxt] == -1 and cap_row[nxt] - flow_row[nxt] > 0:
                level[nxt] = next_level
                if nxt == sink:
                    return True
                q.append(nxt)

    return level[sink] != -1


def dinic_dfs(capacity, flow, level, idx, sink, work, current_flow=INF):
    # DFS function for Dinic algorithm.
    # Finds new flow using edges that is not full.
    if idx == sink:
        return current_flow

    vertices = len(capacity)
    cap_row = capacity[idx]
    flow_row = flow[idx]

    while work[idx] < vertices:
        nxt = work[idx]
        residual = cap_row[nxt] - flow_row[nxt]

        if level[nxt] == level[idx] + 1 and residual > 0:
            pushed = dinic_dfs(capacity, flow, level, nxt, sink, work, min(current_flow, residual))
            if pushed:
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
    flow = _init_flow(vertices)
    ret = 0

    while True:
        level = [-1] * vertices
        if not dinic_bfs(capacity, flow, level, source, sink):
            return ret

        work = [0] * vertices
        while True:
            pushed = dinic_dfs(capacity, flow, level, source, sink, work)
            if not pushed:
                break
            ret += pushed


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