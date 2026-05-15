from collections import deque

graph = {'A': set(['B', 'C', 'F']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['A', 'C', 'E'])}

def traverse(graph, start, use_stack=True):
    """
    Traverse the graph using DFS or BFS.

    Args:
    graph (dict): The graph to traverse.
    start (str): The starting node.
    use_stack (bool): Whether to use a stack (DFS) or a queue (BFS).

    Returns:
    set: The visited nodes.
    """
    visited = set()
    data_structure = deque([start]) if not use_stack else [start]

    while data_structure:
        if use_stack:
            node = data_structure.pop()
        else:
            node = data_structure.popleft()

        if node not in visited:
            visited.add(node)
            for next_node in graph[node]:
                if next_node not in visited:
                    if use_stack:
                        data_structure.append(next_node)
                    else:
                        data_structure.append(next_node)

    return visited

def dfs_traverse_recursive(graph, start, visited=None):
    """
    Traverse the graph using recursive DFS.

    Args:
    graph (dict): The graph to traverse.
    start (str): The starting node.
    visited (set): The visited nodes.

    Returns:
    set: The visited nodes.
    """
    if visited is None:
        visited = set()
    visited.add(start)
    for next_node in graph[start]:
        if next_node not in visited:
            dfs_traverse_recursive(graph, next_node, visited)
    return visited

if __name__ == "__main__":
    print("DFS:", sorted(traverse(graph, 'A')))
    print("BFS:", sorted(traverse(graph, 'A', use_stack=False)))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))