graph = {'A': set(['B', 'C', 'F']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['A', 'C', 'E'])}

def dfs_traverse(graph, start):
    visited, stack = set(), [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            # Use list to avoid multiple set operations
            # Add nodes in reverse order to maintain left-to-right traversal
            stack.extend(reversed(list(graph[node] - visited)))
    return visited

def bfs_traverse(graph, start):
    visited, queue = set(), [start]
    front = 0  # Queue front index pointer
    while front < len(queue):
        node = queue[front]
        front += 1
        if node not in visited:
            visited.add(node)
            # Add unvisited neighbors to queue
            for nextNode in graph[node]:
                if nextNode not in visited:
                    queue.append(nextNode)
    return visited

def dfs_traverse_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    # Process unvisited neighbors directly
    for nextNode in graph[start]:
        if nextNode not in visited:
            dfs_traverse_recursive(graph, nextNode, visited)
    return visited

if __name__ == "__main__":
    print("DFS:", sorted(dfs_traverse(graph, 'A')))
    print("BFS:", sorted(bfs_traverse(graph, 'A')))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))