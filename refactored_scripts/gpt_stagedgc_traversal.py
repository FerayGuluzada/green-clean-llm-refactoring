graph = {
    'A': {'B', 'C', 'F'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'A', 'C', 'E'},
}

# dfs and bfs are the ultimately same except that they are visiting nodes in
# different order. To simulate this ordering we would use stack for dfs and
# queue for bfs.
#

def _traverse(graph, start, depth_first):
    visited = {start}
    pending = [start]
    index = 0
    get_neighbors = graph.get
    add_visited = visited.add
    append_pending = pending.append
    pop_pending = pending.pop

    while pending:
        if depth_first:
            node = pop_pending()
        else:
            if index >= len(pending):
                break
            node = pending[index]
            index += 1

        for neighbor in get_neighbors(node, ()):
            if neighbor not in visited:
                add_visited(neighbor)
                append_pending(neighbor)

    return visited


def dfs_traverse(graph, start):
    return _traverse(graph, start, depth_first=True)


def bfs_traverse(graph, start):
    return _traverse(graph, start, depth_first=False)


def dfs_traverse_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)
    for neighbor in graph.get(start, ()):
        if neighbor not in visited:
            dfs_traverse_recursive(graph, neighbor, visited)
    return visited

# print(dfs_traverse(graph, 'A'))
# print(bfs_traverse(graph, 'A'))
# print(dfs_traverse_recursive(graph, 'A'))

# def find_path(graph, start, end, visited=[]):
#     # basecase
#     visitied = visited + [start]
#     if start == end:
#         return visited
#     if start not in graph:
#         return None
#     for node in graph[start]:
#         if node not in visited:
#             new_visited = find_path(graph, node, end, visited)
#             return new_visited
#     return None

# print(find_path(graph, 'A', 'F'))

if __name__ == "__main__":
    print("DFS:", sorted(dfs_traverse(graph, 'A')))
    print("BFS:", sorted(bfs_traverse(graph, 'A')))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))