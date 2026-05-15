from collections import deque

graph = {'A': set(['B', 'C', 'F']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['A', 'C', 'E'])}

def traverse(graph, start, data_structure):
    """
    Traverse the graph using the given data structure.

    Args:
    graph (dict): The graph to traverse.
    start (str): The starting node.
    data_structure (list or deque): The data structure to use for traversal.

    Returns:
    set: The visited nodes.
    """
    visited = set()
    data_structure.append(start)
    while data_structure:
        # Use a single method to pop the node, reducing the number of isinstance checks
        node = data_structure.pop() if isinstance(data_structure, list) else data_structure.popleft()
        if node not in visited:
            visited.add(node)
            # Use a set comprehension to filter unvisited nodes, reducing the number of if checks
            unvisited_neighbors = {next_node for next_node in graph[node] if next_node not in visited}
            # Use extend to add multiple nodes at once, reducing the number of append calls
            data_structure.extend(unvisited_neighbors) if isinstance(data_structure, list) else data_structure.extendleft(reversed(unvisited_neighbors))
    return visited

def dfs_traverse(graph, start):
    """
    Traverse the graph using Depth-First Search.

    Args:
    graph (dict): The graph to traverse.
    start (str): The starting node.

    Returns:
    set: The visited nodes.
    """
    return traverse(graph, start, [])

def bfs_traverse(graph, start):
    """
    Traverse the graph using Breadth-First Search.

    Args:
    graph (dict): The graph to traverse.
    start (str): The starting node.

    Returns:
    set: The visited nodes.
    """
    return traverse(graph, start, deque())

def dfs_traverse_recursive(graph, start, visited=None):
    """
    Traverse the graph using Depth-First Search recursively.

    Args:
    graph (dict): The graph to traverse.
    start (str): The starting node.
    visited (set, optional): The visited nodes. Defaults to None.

    Returns:
    set: The visited nodes.
    """
    if visited is None:
        visited = set()
    visited.add(start)
    # Use a set comprehension to filter unvisited nodes, reducing the number of if checks
    unvisited_neighbors = {next_node for next_node in graph[start] if next_node not in visited}
    # Use a loop to recursively traverse unvisited neighbors, reducing the number of function calls
    for next_node in unvisited_neighbors:
        dfs_traverse_recursive(graph, next_node, visited)
    return visited

if __name__ == "__main__":
    print("DFS:", sorted(dfs_traverse(graph, 'A')))
    print("BFS:", sorted(bfs_traverse(graph, 'A')))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))