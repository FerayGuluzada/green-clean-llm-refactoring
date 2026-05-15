graph = {'A': set(['B', 'C', 'F']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['A', 'C', 'E'])}

def traverse(graph, start, traversal_type):
    """
    Performs a graph traversal.

    Args:
    graph (dict): The graph represented as an adjacency list.
    start (str): The starting node for the traversal.
    traversal_type (str): The type of traversal, either 'dfs' or 'bfs'.

    Returns:
    set: A set of visited nodes.
    """
    visited, traversal_data_structure = set(), [start]
    if traversal_type == 'dfs':
        traversal_data_structure.pop()
    else:
        traversal_data_structure.pop(0)

    while traversal_data_structure:
        if traversal_type == 'dfs':
            node = traversal_data_structure.pop()
        else:
            node = traversal_data_structure.pop(0)
        if node not in visited:
            visited.add(node)
            # Use list comprehension to filter unvisited neighbors
            if traversal_type == 'dfs':
                traversal_data_structure.extend(nextNode for nextNode in graph[node] if nextNode not in visited)
            else:
                traversal_data_structure.extend(nextNode for nextNode in graph[node] if nextNode not in visited)
    return visited

def traverse_recursive(graph, start, visited=None, traversal_type='dfs'):
    """
    Performs a recursive graph traversal.

    Args:
    graph (dict): The graph represented as an adjacency list.
    start (str): The starting node for the traversal.
    visited (set, optional): A set of visited nodes. Defaults to None.
    traversal_type (str, optional): The type of traversal, either 'dfs' or 'bfs'. Defaults to 'dfs'.

    Returns:
    set: A set of visited nodes.
    """
    if visited is None:
        visited = set()
    visited.add(start)
    # Use a generator expression to recursively visit unvisited neighbors
    for nextNode in (nextNode for nextNode in graph[start] if nextNode not in visited):
        traverse_recursive(graph, nextNode, visited, traversal_type)
    return visited

if __name__ == "__main__":
    print("DFS:", sorted(traverse(graph, 'A', 'dfs')))
    print("BFS:", sorted(traverse(graph, 'A', 'bfs')))
    print("DFS Recursive:", sorted(traverse_recursive(graph, 'A')))