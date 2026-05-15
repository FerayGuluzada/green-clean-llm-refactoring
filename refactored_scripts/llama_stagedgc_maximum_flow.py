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

class MaxFlow:
    def __init__(self, capacity):
        self.capacity = capacity
        self.vertices = len(capacity)
        self.flow = [[0]*self.vertices for _ in range(self.vertices)]

    def _bfs(self, source, sink):
        """BFS function to check if sink is reachable from source."""
        q = queue.Queue()
        q.put(source)
        level = [-1]*self.vertices
        level[source] = 0
        while q.qsize():
            front = q.get()
            for nxt in range(self.vertices):
                if level[nxt] == -1 and self.flow[front][nxt] < self.capacity[front][nxt]:
                    level[nxt] = level[front] + 1
                    q.put(nxt)
        return level[sink]!= -1

    def _dfs(self, capacity, flow, level, idx, sink, current_flow):
        """DFS function to find new flow using edges that are not full."""
        if idx == sink:
            return current_flow
        for nxt in range(self.vertices):
            if level[nxt] == level[idx] + 1 and flow[idx][nxt] < capacity[idx][nxt]:
                tmp = self._dfs(capacity, flow, level, nxt, sink, min(current_flow, capacity[idx][nxt] - flow[idx][nxt]))
                if tmp > 0:
                    flow[idx][nxt] += tmp
                    flow[nxt][idx] -= tmp
                    return tmp
        return 0

    def _edmonds_karp_bfs(self, source, sink):
        """BFS function for Edmonds-Karp algorithm."""
        q = queue.Queue()
        q.put((source, float('inf')))
        visit = [False]*self.vertices
        par = [-1]*self.vertices
        visit[source] = True
        while q.qsize():
            front = q.get()
            idx, current_flow = front
            if idx == sink:
                return par, current_flow
            for nxt in range(self.vertices):
                if not visit[nxt] and self.flow[idx][nxt] < self.capacity[idx][nxt]:
                    visit[nxt] = True
                    par[nxt] = idx
                    q.put((nxt, min(current_flow, self.capacity[idx][nxt]-self.flow[idx][nxt])))
        return par, 0

    def ford_fulkerson(self, source, sink):
        """Computes maximum flow from source to sink using DFS."""
        ret = 0
        while True:
            visit = [False]*self.vertices
            tmp = self._dfs(self.capacity, self.flow, visit, source, sink, float('inf'))
            if tmp:
                ret += tmp
            else:
                break
        return ret

    def edmonds_karp(self, source, sink):
        """Computes maximum flow from source to sink using BFS."""
        ret = 0
        while True:
            par, tmp = self._edmonds_karp_bfs(source, sink)
            if tmp == 0:
                break
            ret += tmp
            idx = sink
            parent = par[sink]
            while parent!= -1:
                self.flow[parent][idx] += tmp
                self.flow[idx][parent] -= tmp
                idx = parent
                parent = par[parent]
        return ret

    def dinic(self, source, sink):
        """Computes maximum flow from source to sink using Dinic algorithm."""
        ret = 0
        while True:
            level = [-1]*self.vertices
            if not self._bfs(source, sink):
                break
            work = [0]*self.vertices
            while True:
                tmp = self._dfs(self.capacity, self.flow, level, source, sink, float('inf'))
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

    max_flow = MaxFlow(capacity)
    print(max_flow.ford_fulkerson(source, sink))
    max_flow = MaxFlow(capacity)
    print(max_flow.edmonds_karp(source, sink))
    max_flow = MaxFlow(capacity)
    print(max_flow.dinic(source, sink))