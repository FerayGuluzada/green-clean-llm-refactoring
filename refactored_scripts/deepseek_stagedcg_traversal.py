graph = {
    'A': {'B', 'C', 'F'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'A', 'C', 'E'}
}

def _traverse(graph, start, data_structure):
    """Generic graph traversal using either stack (DFS) or queue (BFS)."""
    visited = set()
    nodes_to_visit = [start]
    
    while nodes_to_visit:
        node = data_structure(nodes_to_visit)
        if node not in visited:
            visited.add(node)
            # Pre-filter neighbors to avoid extending with already visited nodes
            unvisited = graph[node] - visited
            if unvisited:
                nodes_to_visit.extend(unvisited)
    
    return visited

def dfs_traverse(graph, start):
    """Depth-First Search using stack (LIFO)."""
    return _traverse(graph, start, lambda lst: lst.pop())

def bfs_traverse(graph, start):
    """Breadth-First Search using queue (FIFO)."""
    # Use collections.deque for O(1) popleft operation
    from collections import deque
    
    visited = set([start])
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        # Process neighbors in one batch
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited

def dfs_traverse_recursive(graph, start, visited=None):
    """Recursive Depth-First Search."""
    if visited is None:
        visited = set()
    
    visited.add(start)
    # Process all neighbors in one iteration
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_traverse_recursive(graph, neighbor, visited)
    
    return visited

if __name__ == "__main__":
    print("DFS:", sorted(dfs_traverse(graph, 'A')))
    print("BFS:", sorted(bfs_traverse(graph, 'A')))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))