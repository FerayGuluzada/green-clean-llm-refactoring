graph = {
    'A': {'B', 'C', 'F'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'A', 'C', 'E'}
}

def _traverse(graph, start, use_stack=True):
    """Unified traversal function for both DFS and BFS.
    
    Args:
        graph: Adjacency list representation
        start: Starting node
        use_stack: True for DFS (LIFO), False for BFS (FIFO)
    
    Returns:
        Set of visited nodes
    """
    visited = set()
    container = [start]
    front = 0  # Index pointer for queue operations
    
    while (use_stack and container) or (not use_stack and front < len(container)):
        if use_stack:
            node = container.pop()
        else:
            node = container[front]
            front += 1
            
        if node not in visited:
            visited.add(node)
            # Add unvisited neighbors
            for neighbor in graph[node]:
                if neighbor not in visited:
                    if use_stack:
                        # DFS: reverse order to maintain original traversal order
                        container.append(neighbor)
                    else:
                        # BFS: append to end
                        container.append(neighbor)
    return visited

def dfs_traverse(graph, start):
    """Depth-First Search using stack."""
    return _traverse(graph, start, use_stack=True)

def bfs_traverse(graph, start):
    """Breadth-First Search using queue."""
    return _traverse(graph, start, use_stack=False)

def dfs_traverse_recursive(graph, start, visited=None):
    """Depth-First Search using recursion."""
    if visited is None:
        visited = set()
    visited.add(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_traverse_recursive(graph, neighbor, visited)
    return visited

if __name__ == "__main__":
    print("DFS:", sorted(dfs_traverse(graph, 'A')))
    print("BFS:", sorted(bfs_traverse(graph, 'A')))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))