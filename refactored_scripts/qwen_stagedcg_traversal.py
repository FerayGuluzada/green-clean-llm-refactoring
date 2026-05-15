graph = {'A': set(['B', 'C', 'F']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['A', 'C', 'E'])}

def dfs_traverse(graph, start):
    """Traverse graph using Depth-First Search starting from `start` node."""
    visited, stack = set(), [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            # Add unvisited neighbors to stack
            stack.extend(graph[node] - visited)
    return visited

def bfs_traverse(graph, start):
    """Traverse graph using Breadth-First Search starting from `start` node."""
    from collections import deque
    visited, queue = set(), deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            # Add unvisited neighbors to queue
            queue.extend(graph[node] - visited)
    return visited

def dfs_traverse_recursive(graph, start, visited=None):
    """Recursively traverse graph using Depth-First Search."""
    if visited is None:
        visited = set()
    visited.add(start)
    # Visit unvisited neighbors recursively
    for next_node in graph[start] - visited:
        dfs_traverse_recursive(graph, next_node, visited)
    return visited

if __name__ == "__main__":
    print("DFS:", sorted(dfs_traverse(graph, 'A')))
    print("BFS:", sorted(bfs_traverse(graph, 'A')))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))