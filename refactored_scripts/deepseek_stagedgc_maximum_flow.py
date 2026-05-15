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
from typing import List

class FlowNetwork:
    """Base class for flow network algorithms."""
    def __init__(self, capacity: List[List[int]]):
        self.capacity = capacity
        self.vertices = len(capacity)
        self.flow = [[0] * self.vertices for _ in range(self.vertices)]
    
    def _reset_flow(self):
        """Reset flow matrix to zero."""
        self.flow = [[0] * self.vertices for _ in range(self.vertices)]


class FordFulkerson(FlowNetwork):
    """Ford-Fulkerson algorithm using DFS."""
    
    def _dfs(self, idx: int, sink: int, visit: List[bool], current_flow: int = 1 << 63) -> int:
        """Depth-first search to find augmenting path."""
        if idx == sink:
            return current_flow
        
        visit[idx] = True
        
        for nxt in range(self.vertices):
            if not visit[nxt]:
                residual = self.capacity[idx][nxt] - self.flow[idx][nxt]
                if residual > 0:
                    tmp = self._dfs(nxt, sink, visit, min(current_flow, residual))
                    if tmp:
                        self.flow[idx][nxt] += tmp
                        self.flow[nxt][idx] -= tmp
                        return tmp
        return 0
    
    def max_flow(self, source: int, sink: int) -> int:
        """Compute maximum flow from source to sink."""
        total_flow = 0
        
        while True:
            visit = [False] * self.vertices
            augment = self._dfs(source, sink, visit)
            if augment:
                total_flow += augment
            else:
                break
        
        return total_flow


class EdmondsKarp(FlowNetwork):
    """Edmonds-Karp algorithm (Ford-Fulkerson with BFS)."""
    
    def _bfs_augmenting_path(self, source: int, sink: int) -> List[int]:
        """Find augmenting path using BFS."""
        q = queue.Queue()
        parent = [-1] * self.vertices
        parent[source] = source
        q.put(source)
        
        while not q.empty():
            u = q.get()
            for v in range(self.vertices):
                if parent[v] == -1 and self.flow[u][v] < self.capacity[u][v]:
                    parent[v] = u
                    if v == sink:
                        return parent
                    q.put(v)
        
        return parent
    
    def _compute_bottleneck(self, parent: List[int], source: int, sink: int) -> int:
        """Compute bottleneck capacity of found path."""
        path_flow = float('inf')
        v = sink
        
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, self.capacity[u][v] - self.flow[u][v])
            v = u
        
        return path_flow
    
    def _update_flow(self, parent: List[int], source: int, sink: int, path_flow: int):
        """Update flow along augmenting path."""
        v = sink
        while v != source:
            u = parent[v]
            self.flow[u][v] += path_flow
            self.flow[v][u] -= path_flow
            v = u
    
    def max_flow(self, source: int, sink: int) -> int:
        """Compute maximum flow from source to sink."""
        total_flow = 0
        
        while True:
            parent = self._bfs_augmenting_path(source, sink)
            if parent[sink] == -1:
                break
            
            path_flow = self._compute_bottleneck(parent, source, sink)
            self._update_flow(parent, source, sink, path_flow)
            total_flow += path_flow
        
        return total_flow


class Dinic(FlowNetwork):
    """Dinic's algorithm with level graph and blocking flow."""
    
    def _bfs_level_graph(self, source: int, sink: int) -> List[int]:
        """Build level graph using BFS."""
        level = [-1] * self.vertices
        q = queue.Queue()
        q.put(source)
        level[source] = 0
        
        while not q.empty():
            u = q.get()
            for v in range(self.vertices):
                if level[v] == -1 and self.flow[u][v] < self.capacity[u][v]:
                    level[v] = level[u] + 1
                    q.put(v)
        
        return level
    
    def _dfs_blocking_flow(self, idx: int, sink: int, level: List[int], 
                          work: List[int], current_flow: int = 1 << 63) -> int:
        """Find blocking flow using DFS on level graph."""
        if idx == sink:
            return current_flow
        
        for i in range(work[idx], self.vertices):
            v = i
            if level[v] == level[idx] + 1 and self.flow[idx][v] < self.capacity[idx][v]:
                residual = self.capacity[idx][v] - self.flow[idx][v]
                tmp = self._dfs_blocking_flow(v, sink, level, work, 
                                             min(current_flow, residual))
                if tmp > 0:
                    self.flow[idx][v] += tmp
                    self.flow[v][idx] -= tmp
                    return tmp
            work[idx] += 1
        
        return 0
    
    def max_flow(self, source: int, sink: int) -> int:
        """Compute maximum flow from source to sink."""
        total_flow = 0
        
        while True:
            level = self._bfs_level_graph(source, sink)
            if level[sink] == -1:
                break
            
            work = [0] * self.vertices
            while True:
                augment = self._dfs_blocking_flow(source, sink, level, work)
                if augment > 0:
                    total_flow += augment
                else:
                    break
        
        return total_flow


def ford_fulkerson(capacity, source, sink):
    """Wrapper for Ford-Fulkerson algorithm."""
    return FordFulkerson(capacity).max_flow(source, sink)

def edmonds_karp(capacity, source, sink):
    """Wrapper for Edmonds-Karp algorithm."""
    return EdmondsKarp(capacity).max_flow(source, sink)

def dinic(capacity, source, sink):
    """Wrapper for Dinic's algorithm."""
    return Dinic(capacity).max_flow(source, sink)


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