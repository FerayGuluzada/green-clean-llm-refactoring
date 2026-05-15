graph = {'A': set(['B', 'C', 'F']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['A', 'C', 'E'])}

def dfs_traverse(graph, start):
    """
    Performs a depth-first search traversal of the graph.
    
    Args:
    graph (dict): The graph represented as an adjacency list.
    start (str): The starting node for the traversal.
    
    Returns:
    set: A set of visited nodes.
    """
    visited, stack = set(), [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            # Use list comprehension to filter unvisited neighbors
            stack.extend([nextNode for nextNode in graph[node] if nextNode not in visited])
    return visited

def bfs_traverse(graph, start):
    """
    Performs a breadth-first search traversal of the graph.
    
    Args:
    graph (dict): The graph represented as an adjacency list.
    start (str): The starting node for the traversal.
    
    Returns:
    set: A set of visited nodes.
    """
    visited, queue = set(), [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            # Use list comprehension to filter unvisited neighbors
            queue.extend([nextNode for nextNode in graph[node] if nextNode not in visited])
    return visited

def dfs_traverse_recursive(graph, start, visited=None):
    """
    Performs a recursive depth-first search traversal of the graph.
    
    Args:
    graph (dict): The graph represented as an adjacency list.
    start (str): The starting node for the traversal.
    visited (set, optional): A set of visited nodes. Defaults to None.
    
    Returns:
    set: A set of visited nodes.
    """
    if visited is None:
        visited = set()
    visited.add(start)
    # Use list comprehension to filter unvisited neighbors
    for nextNode in [node for node in graph[start] if node not in visited]:
        dfs_traverse_recursive(graph, nextNode, visited)
    return visited

if __name__ == "__main__":
    print("DFS:", sorted(dfs_traverse(graph, 'A')))
    print("BFS:", sorted(bfs_traverse(graph, 'A')))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))