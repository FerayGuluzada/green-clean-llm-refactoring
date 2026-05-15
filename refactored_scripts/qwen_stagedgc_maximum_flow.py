"""
Given the capacity, source and sink of a graph,
computes the maximum flow from source to sink.
Input : capacity, source, sink
Output : maximum flow from source to sink
Capacity is a two-dimensional array that is v*v.
capacity[i][j] implies the capacity of the edge from i to j.
If there is no edge from i to j, capacity[i][j] should be zero.
"""

import collections

def dfs(capacity, flow, visit, vertices, idx, sink, current_flow):
    """DFS function for ford_fulkerson algorithm."""
    if idx == sink: 
        return current_flow
    visit[idx] = True
    for nxt in range(vertices):
        if not visit[nxt] and flow[idx][nxt] < capacity[idx][nxt]:
            tmp = dfs(capacity, flow, visit, vertices, nxt, sink, 
                     min(current_flow, capacity[idx][nxt]-flow[idx][nxt]))
            if tmp:
                flow[idx][nxt] += tmp
                flow[nxt][idx] -= tmp
                return tmp
    return 0

def ford_fulkerson(capacity, source, sink):
    """Computes maximum flow from source to sink using DFS. Time Complexity : O(Ef)"""
    vertices = len(capacity)
    ret = 0
    flow = [[0] * vertices for _ in range(vertices)]
    visit = [False] * vertices
    
    while True:
        # Reuse visit array instead of recreating
        for i in range(vertices):
            visit[i] = False
        tmp = dfs(capacity, flow, visit, vertices, source, sink, float('inf'))
        if tmp: 
            ret += tmp
        else: 
            break
    return ret

def edmonds_karp(capacity, source, sink):
    """Computes maximum flow from source to sink using BFS. Time complexity : O(V*E^2)"""
    vertices = len(capacity)
    ret = 0
    flow = [[0] * vertices for _ in range(vertices)]
    
    while True:
        tmp = 0
        q = collections.deque()
        visit = [False] * vertices
        par = [-1] * vertices
        visit[source] = True
        q.append((source, float('inf')))
        
        # Finds new flow using BFS.
        while q:
            idx, current_flow = q.popleft()
            if idx == sink:
                tmp = current_flow
                break
            for nxt in range(vertices):
                if not visit[nxt] and flow[idx][nxt] < capacity[idx][nxt]:
                    visit[nxt] = True
                    par[nxt] = idx
                    q.append((nxt, min(current_flow, capacity[idx][nxt]-flow[idx][nxt])))
        
        if par[sink] == -1: 
            break
        ret += tmp
        parent = par[sink]
        idx = sink
        # Update flow array following parent starting from sink.
        while parent != -1:
            flow[parent][idx] += tmp
            flow[idx][parent] -= tmp
            idx = parent
            parent = par[parent]
    return ret

def dinic_bfs(capacity, flow, level, source, sink):
    """BFS function for Dinic algorithm. Check whether sink is reachable only using edges that is not full."""
    vertices = len(capacity)
    q = collections.deque()
    q.append(source)
    level[source] = 0
    
    while q:
        front = q.popleft()
        for nxt in range(vertices):
            if level[nxt] == -1 and flow[front][nxt] < capacity[front][nxt]:
                level[nxt] = level[front] + 1
                q.append(nxt)
    return level[sink] != -1

def dinic_dfs(capacity, flow, level, idx, sink, work, current_flow):
    """DFS function for Dinic algorithm. Finds new flow using edges that is not full."""
    if idx == sink:
        return current_flow
    vertices = len(capacity)
    
    while work[idx] < vertices:
        nxt = work[idx]
        if level[nxt] == level[idx] + 1 and flow[idx][nxt] < capacity[idx][nxt]:
            tmp = dinic_dfs(capacity, flow, level, nxt, sink, work, 
                           min(current_flow, capacity[idx][nxt] - flow[idx][nxt])) 
            if tmp > 0:
                flow[idx][nxt] += tmp
                flow[nxt][idx] -= tmp
                return tmp
        work[idx] += 1
    return 0

def dinic(capacity, source, sink):
    """Computes maximum flow from source to sink using Dinic algorithm. Time complexity : O(V^2*E)"""
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    ret = 0
    
    level = [-1] * vertices
    work = [0] * vertices
    
    while True:
        # Reset arrays instead of recreating
        for i in range(vertices):
            level[i] = -1
        for i in range(vertices):
            work[i] = 0
            
        if not dinic_bfs(capacity, flow, level, source, sink):
            break
            
        while True:
            tmp = dinic_dfs(capacity, flow, level, source, sink, work, float('inf'))
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