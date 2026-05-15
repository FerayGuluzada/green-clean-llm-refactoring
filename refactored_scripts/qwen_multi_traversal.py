graph = {
    'A': {'B', 'C', 'F'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'A', 'C', 'E'}
}

def _traverse_graph(graph, start, use_stack=True):
    """
    Generic graph traversal function.
    
    Args:
        graph: Dictionary representing the graph
        start: Starting node
        use_stack: If True, uses DFS (stack); if False, uses BFS (queue)
    """
    visited, structure = set(), [start]
    
    while structure:
        # Pop from end for stack (DFS), from beginning for queue (BFS)
        node = structure.pop() if use_stack else structure.pop(0)
        
        if node not in visited:
            visited.add(node)
            # Add unvisited neighbors to structure
            for neighbor in graph.get(node, set()):
                if neighbor not in visited:
                    structure.append(neighbor)
                    
    return visited

def dfs_traverse(graph, start):
    """Depth-First Search traversal using iterative approach."""
    return _traverse_graph(graph, start, use_stack=True)

def bfs_traverse(graph, start):
    """Breadth-First Search traversal using iterative approach."""
    return _traverse_graph(graph, start, use_stack=False)

def dfs_traverse_recursive(graph, start, visited=None):
    """Depth-First Search traversal using recursive approach."""
    if visited is None:
        visited = set()
        
    visited.add(start)
    
    for neighbor in graph.get(start, set()):
        if neighbor not in visited:
            dfs_traverse_recursive(graph, neighbor, visited)
            
    return visited

if __name__ == "__main__":
    print("DFS:", sorted(dfs_traverse(graph, 'A')))
    print("BFS:", sorted(bfs_traverse(graph, 'A')))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))