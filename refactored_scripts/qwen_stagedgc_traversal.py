graph = {
    'A': {'B', 'C', 'F'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'A', 'C', 'E'}
}

def dfs_traverse(graph, start):
    """Iterative DFS traversal using stack."""
    visited, stack = set(), [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            # Add unvisited neighbors in reverse order for correct traversal
            stack.extend(reversed(list(graph[node] - visited)))
    return visited

def bfs_traverse(graph, start):
    """BFS traversal using index-based queue simulation."""
    visited, queue = set(), [start]
    front = 0
    while front < len(queue):
        node = queue[front]
        front += 1
        if node not in visited:
            visited.add(node)
            # Add unvisited neighbors to queue
            queue.extend(neighbor for neighbor in graph[node] 
                        if neighbor not in visited)
    return visited

def dfs_traverse_recursive(graph, start, visited=None):
    """Recursive DFS traversal."""
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