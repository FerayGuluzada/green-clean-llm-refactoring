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

def dfs(capacity, flow, visit, vertices, idx, sink, current_flow):
    """DFS function for Ford-Fulkerson algorithm."""
    if idx == sink:
        return current_flow
    
    visit[idx] = True
    for nxt in range(vertices):
        if not visit[nxt] and flow[idx][nxt] < capacity[idx][nxt]:
            bottleneck = min(current_flow, capacity[idx][nxt] - flow[idx][nxt])
            tmp = dfs(capacity, flow, visit, vertices, nxt, sink, bottleneck)
            if tmp > 0:
                flow[idx][nxt] += tmp
                flow[nxt][idx] -= tmp
                return tmp
    return 0

def ford_fulkerson(capacity, source, sink):
    """
    Computes maximum flow from source to sink using DFS.
    Time Complexity : O(Ef)
    E is the number of edges and f is the maximum flow in the graph.
    """
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0
    
    while True:
        visit = [False] * vertices
        flow_increment = dfs(capacity, flow, visit, vertices, source, sink, float('inf'))
        if flow_increment == 0:
            break
        max_flow += flow_increment
    
    return max_flow

def edmonds_karp(capacity, source, sink):
    """
    Computes maximum flow from source to sink using BFS.
    Time complexity : O(V*E^2)
    V is the number of vertices and E is the number of edges.
    """
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0
    
    while True:
        # BFS to find augmenting path
        q = queue.Queue()
        visit = [False] * vertices
        parent = [-1] * vertices
        visit[source] = True
        q.put((source, float('inf')))
        
        bottleneck = 0
        while not q.empty():
            idx, current_flow = q.get()
            if idx == sink:
                bottleneck = current_flow
                break
                
            for nxt in range(vertices):
                if not visit[nxt] and flow[idx][nxt] < capacity[idx][nxt]:
                    visit[nxt] = True
                    parent[nxt] = idx
                    new_flow = min(current_flow, capacity[idx][nxt] - flow[idx][nxt])
                    q.put((nxt, new_flow))
        
        if bottleneck == 0:
            break
            
        # Update flow along the path
        max_flow += bottleneck
        current = sink
        while current != source:
            prev = parent[current]
            flow[prev][current] += bottleneck
            flow[current][prev] -= bottleneck
            current = prev
    
    return max_flow

def dinic_bfs(capacity, flow, level, source, sink):
    """
    BFS function for Dinic algorithm.
    Check whether sink is reachable only using edges that are not full.
    """
    vertices = len(capacity)
    q = queue.Queue()
    q.put(source)
    level[source] = 0
    
    while not q.empty():
        node = q.get()
        for nxt in range(vertices):
            if level[nxt] == -1 and flow[node][nxt] < capacity[node][nxt]:
                level[nxt] = level[node] + 1
                q.put(nxt)
    
    return level[sink] != -1

def dinic_dfs(capacity, flow, level, idx, sink, work, current_flow):
    """DFS function for Dinic algorithm. Finds new flow using edges that are not full."""
    if idx == sink:
        return current_flow
    
    vertices = len(capacity)
    while work[idx] < vertices:
        nxt = work[idx]
        if level[nxt] == level[idx] + 1 and flow[idx][nxt] < capacity[idx][nxt]:
            bottleneck = min(current_flow, capacity[idx][nxt] - flow[idx][nxt])
            flow_increment = dinic_dfs(capacity, flow, level, nxt, sink, work, bottleneck)
            if flow_increment > 0:
                flow[idx][nxt] += flow_increment
                flow[nxt][idx] -= flow_increment
                return flow_increment
        work[idx] += 1
    
    return 0

def dinic(capacity, source, sink):
    """
    Computes maximum flow from source to sink using Dinic algorithm.
    Time complexity : O(V^2*E)
    V is the number of vertices and E is the number of edges.
    """
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]
    max_flow = 0
    
    while True:
        level = [-1] * vertices
        work = [0] * vertices
        if not dinic_bfs(capacity, flow, level, source, sink):
            break
            
        while True:
            flow_increment = dinic_dfs(capacity, flow, level, source, sink, work, float('inf'))
            if flow_increment == 0:
                break
            max_flow += flow_increment
    
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