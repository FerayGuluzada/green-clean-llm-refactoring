graph = {'A': set(['B', 'C', 'F']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['A', 'C', 'E'])}

def _traverse(graph, start, data_structure):
    """Generic traversal using either stack (DFS) or queue (BFS)."""
    visited = set()
    container = [start]
    
    while container:
        node = data_structure(container)
        if node not in visited:
            visited.add(node)
            # Add unvisited neighbors to container
            container.extend(graph[node] - visited)
    return visited

def dfs_traverse(graph, start):
    """Depth-First Search using stack (LIFO)."""
    return _traverse(graph, start, lambda c: c.pop())

def bfs_traverse(graph, start):
    """Breadth-First Search using queue (FIFO)."""
    return _traverse(graph, start, lambda c: c.pop(0))

def dfs_traverse_recursive(graph, start, visited=None):
    """Recursive DFS implementation."""
    if visited is None:
        visited = set()
    visited.add(start)
    
    for neighbor in graph[start] - visited:
        dfs_traverse_recursive(graph, neighbor, visited)
    return visited

if __name__ == "__main__":
    print("DFS:", sorted(dfs_traverse(graph, 'A')))
    print("BFS:", sorted(bfs_traverse(graph, 'A')))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))