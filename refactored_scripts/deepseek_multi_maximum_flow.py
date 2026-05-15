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

def _dfs_augment(capacity, flow, visited, vertices, idx, sink, current_flow=float('inf')):
    """DFS for finding augmenting paths in Ford-Fulkerson."""
    if idx == sink:
        return current_flow
    visited[idx] = True
    for nxt in range(vertices):
        if not visited[nxt] and flow[idx][nxt] < capacity[idx][nxt]:
            residual = capacity[idx][nxt] - flow[idx][nxt]
            augment = _dfs_augment(capacity, flow, visited, vertices, nxt, sink,
                                 min(current_flow, residual))
            if augment:
                flow[idx][nxt] += augment
                flow[nxt][idx] -= augment
                return augment
    return 0

def ford_fulkerson(capacity, source, sink):
    """
    Maximum flow using DFS augmenting paths.
    Time Complexity: O(E * f) where E is edges, f is max flow.
    """
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0
    
    while True:
        visited = [False] * vertices
        augment = _dfs_augment(capacity, flow, visited, vertices, source, sink)
        if not augment:
            break
        max_flow += augment
    return max_flow

def edmonds_karp(capacity, source, sink):
    """
    Maximum flow using BFS augmenting paths (Edmonds-Karp).
    Time Complexity: O(V * E^2)
    """
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0
    
    while True:
        parent = [-1] * vertices
        parent[source] = source
        q = queue.Queue()
        q.put((source, float('inf')))
        
        # BFS for augmenting path
        while not q.empty():
            idx, current_flow = q.get()
            for nxt in range(vertices):
                if parent[nxt] == -1 and flow[idx][nxt] < capacity[idx][nxt]:
                    residual = capacity[idx][nxt] - flow[idx][nxt]
                    parent[nxt] = idx
                    new_flow = min(current_flow, residual)
                    if nxt == sink:
                        augment = new_flow
                        max_flow += augment
                        # Update flow along path
                        while nxt != source:
                            prev = parent[nxt]
                            flow[prev][nxt] += augment
                            flow[nxt][prev] -= augment
                            nxt = prev
                        break
                    q.put((nxt, new_flow))
            else:
                continue
            break
        else:
            break  # No augmenting path found
    return max_flow

def _dinic_bfs(capacity, flow, level, source, sink):
    """BFS for level graph construction in Dinic."""
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

def _dinic_dfs(capacity, flow, level, idx, sink, work, current_flow=float('inf')):
    """DFS for blocking flow computation in Dinic."""
    if idx == sink:
        return current_flow
    
    vertices = len(capacity)
    while work[idx] < vertices:
        v = work[idx]
        if level[v] == level[idx] + 1 and flow[idx][v] < capacity[idx][v]:
            residual = capacity[idx][v] - flow[idx][v]
            augment = _dinic_dfs(capacity, flow, level, v, sink, work,
                               min(current_flow, residual))
            if augment:
                flow[idx][v] += augment
                flow[v][idx] -= augment
                return augment
        work[idx] += 1
    return 0

def dinic(capacity, source, sink):
    """
    Maximum flow using Dinic's algorithm.
    Time Complexity: O(V^2 * E)
    """
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0
    
    while True:
        level = [-1] * vertices
        if not _dinic_bfs(capacity, flow, level, source, sink):
            break
        
        work = [0] * vertices
        while True:
            augment = _dinic_dfs(capacity, flow, level, source, sink, work)
            if not augment:
                break
            max_flow += augment
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
    source, sink = 0, 5
    
    print(ford_fulkerson(capacity, source, sink))
    print(edmonds_karp(capacity, source, sink))
    print(dinic(capacity, source, sink))