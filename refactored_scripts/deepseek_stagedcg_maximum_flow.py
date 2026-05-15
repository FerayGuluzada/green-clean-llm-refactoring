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

def _dfs_augment(capacity, flow, visited, vertices, idx, sink, current_flow=1 << 63):
    """DFS function for ford_fulkerson algorithm."""
    if idx == sink:
        return current_flow
    
    visited[idx] = True
    # Precompute neighbors with residual capacity
    for nxt in range(vertices):
        if not visited[nxt]:
            residual = capacity[idx][nxt] - flow[idx][nxt]
            if residual > 0:
                augmenting_flow = _dfs_augment(
                    capacity, flow, visited, vertices, nxt, sink,
                    current_flow if current_flow < residual else residual
                )
                if augmenting_flow:
                    flow[idx][nxt] += augmenting_flow
                    flow[nxt][idx] -= augmenting_flow
                    return augmenting_flow
    return 0

def ford_fulkerson(capacity, source, sink):
    """
    Computes maximum flow from source to sink using DFS.
    Time Complexity: O(Ef) where E is edges and f is maximum flow.
    """
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0
    
    while True:
        visited = [False] * vertices
        augmenting_flow = _dfs_augment(capacity, flow, visited, vertices, source, sink)
        if not augmenting_flow:
            break
        max_flow += augmenting_flow
    
    return max_flow

def _bfs_augmenting_path(capacity, flow, source, sink):
    """Finds augmenting path using BFS for Edmonds-Karp."""
    vertices = len(capacity)
    visited = [False] * vertices
    parent = [-1] * vertices
    q = queue.Queue()
    
    visited[source] = True
    q.put((source, float('inf')))
    
    while not q.empty():
        idx, current_flow = q.get()
        if idx == sink:
            return current_flow, parent
        
        # Check neighbors with residual capacity
        for nxt in range(vertices):
            if not visited[nxt]:
                residual = capacity[idx][nxt] - flow[idx][nxt]
                if residual > 0:
                    visited[nxt] = True
                    parent[nxt] = idx
                    q.put((nxt, current_flow if current_flow < residual else residual))
    
    return 0, parent

def _update_flow(flow, parent, sink, augmenting_flow):
    """Updates flow along augmenting path."""
    idx = sink
    while parent[idx] != -1:
        parent_idx = parent[idx]
        flow[parent_idx][idx] += augmenting_flow
        flow[idx][parent_idx] -= augmenting_flow
        idx = parent_idx

def edmonds_karp(capacity, source, sink):
    """
    Computes maximum flow from source to sink using BFS.
    Time complexity: O(V*E^2)
    """
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0
    
    while True:
        augmenting_flow, parent = _bfs_augmenting_path(capacity, flow, source, sink)
        if parent[sink] == -1:
            break
        
        max_flow += augmenting_flow
        _update_flow(flow, parent, sink, augmenting_flow)
    
    return max_flow

def _dinic_bfs(capacity, flow, source, sink):
    """BFS for Dinic to build level graph."""
    vertices = len(capacity)
    level = [-1] * vertices
    q = queue.Queue()
    
    level[source] = 0
    q.put(source)
    
    while not q.empty():
        idx = q.get()
        # Only check edges with residual capacity
        for nxt in range(vertices):
            if level[nxt] == -1:
                residual = capacity[idx][nxt] - flow[idx][nxt]
                if residual > 0:
                    level[nxt] = level[idx] + 1
                    q.put(nxt)
    
    return level[sink] != -1, level

def _dinic_dfs(capacity, flow, level, idx, sink, work, current_flow=float('inf')):
    """DFS for Dinic to find blocking flow."""
    if idx == sink:
        return current_flow
    
    vertices = len(capacity)
    while work[idx] < vertices:
        nxt = work[idx]
        if level[nxt] == level[idx] + 1:
            residual = capacity[idx][nxt] - flow[idx][nxt]
            if residual > 0:
                augmenting_flow = _dinic_dfs(
                    capacity, flow, level, nxt, sink, work,
                    current_flow if current_flow < residual else residual
                )
                if augmenting_flow:
                    flow[idx][nxt] += augmenting_flow
                    flow[nxt][idx] -= augmenting_flow
                    return augmenting_flow
        work[idx] += 1
    return 0

def dinic(capacity, source, sink):
    """
    Computes maximum flow from source to sink using Dinic algorithm.
    Time complexity: O(V^2*E)
    """
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0
    
    while True:
        reachable, level = _dinic_bfs(capacity, flow, source, sink)
        if not reachable:
            break
        
        work = [0] * vertices
        while True:
            augmenting_flow = _dinic_dfs(capacity, flow, level, source, sink, work)
            if not augmenting_flow:
                break
            max_flow += augmenting_flow
    
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