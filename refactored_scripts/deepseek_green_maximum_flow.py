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

def dfs(capacity, flow, visit, vertices, idx, sink, current_flow=1 << 63):
    # DFS function for ford_fulkerson algorithm.
    if idx == sink:
        return current_flow
    visit[idx] = True
    for nxt in range(vertices):
        if not visit[nxt]:
            residual = capacity[idx][nxt] - flow[idx][nxt]
            if residual > 0:
                tmp = dfs(capacity, flow, visit, vertices, nxt, sink,
                         min(current_flow, residual))
                if tmp:
                    flow[idx][nxt] += tmp
                    flow[nxt][idx] -= tmp
                    return tmp
    return 0

def ford_fulkerson(capacity, source, sink):
    # Computes maximum flow from source to sink using DFS.
    # Time Complexity : O(Ef)
    # E is the number of edges and f is the maximum flow in the graph.
    vertices = len(capacity)
    ret = 0
    flow = [[0] * vertices for _ in range(vertices)]
    while True:
        visit = [False] * vertices
        tmp = dfs(capacity, flow, visit, vertices, source, sink)
        if tmp:
            ret += tmp
        else:
            break
    return ret

def edmonds_karp(capacity, source, sink):
    # Computes maximum flow from source to sink using BFS.
    # Time complexity : O(V*E^2)
    # V is the number of vertices and E is the number of edges.
    vertices = len(capacity)
    ret = 0
    flow = [[0] * vertices for _ in range(vertices)]
    while True:
        q = queue.Queue()
        parent = [-1] * vertices
        parent[source] = source
        q.put(source)
        
        # BFS to find augmenting path
        while not q.empty():
            u = q.get()
            if u == sink:
                break
            for v in range(vertices):
                if parent[v] == -1 and flow[u][v] < capacity[u][v]:
                    parent[v] = u
                    q.put(v)
        
        if parent[sink] == -1:
            break
            
        # Find bottleneck capacity
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v] - flow[u][v])
            v = u
            
        # Update flow
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u
            
        ret += path_flow
    return ret

def dinic_bfs(capacity, flow, level, source, sink):
    # BFS function for Dinic algorithm.
    # Check whether sink is reachable only using edges that is not full.
    vertices = len(capacity)
    q = queue.Queue()
    q.put(source)
    level[source] = 0
    while not q.empty():
        u = q.get()
        for v in range(vertices):
            if level[v] == -1 and flow[u][v] < capacity[u][v]:
                level[v] = level[u] + 1
                q.put(v)
    return level[sink] != -1

def dinic_dfs(capacity, flow, level, idx, sink, work, current_flow=1 << 63):
    # DFS function for Dinic algorithm.
    # Finds new flow using edges that is not full.
    if idx == sink:
        return current_flow
    vertices = len(capacity)
    for v in range(work[idx], vertices):
        if level[v] == level[idx] + 1 and flow[idx][v] < capacity[idx][v]:
            tmp = dinic_dfs(capacity, flow, level, v, sink, work,
                           min(current_flow, capacity[idx][v] - flow[idx][v]))
            if tmp > 0:
                flow[idx][v] += tmp
                flow[v][idx] -= tmp
                return tmp
        work[idx] += 1
    return 0

def dinic(capacity, source, sink):
    # Computes maximum flow from source to sink using Dinic algorithm.
    # Time complexity : O(V^2*E)
    # V is the number of vertices and E is the number of edges.
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    ret = 0
    while True:
        level = [-1] * vertices
        if not dinic_bfs(capacity, flow, level, source, sink):
            break
        work = [0] * vertices
        while True:
            tmp = dinic_dfs(capacity, flow, level, source, sink, work)
            if tmp > 0:
                ret += tmp
            else:
                break
    return ret

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