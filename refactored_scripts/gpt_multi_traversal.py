from collections import deque

graph = {'A': {'B', 'C', 'F'},
         'B': {'A', 'D', 'E'},
         'C': {'A', 'F'},
         'D': {'B'},
         'E': {'B', 'F'},
         'F': {'A', 'C', 'E'}}

# dfs and bfs are the ultimately same except that they are visiting nodes in
# different order. To simulate this ordering we would use stack for dfs and
# queue for bfs.
#


def _traverse(graph, start, pop_next):
    visited = set()
    pending = pop_next.__self__
    while pending:
        node = pop_next()
        if node in visited:
            continue
        visited.add(node)
        pending.extend(next_node for next_node in graph[node] if next_node not in visited)
    return visited


def dfs_traverse(graph, start):
    return _traverse(graph, start, [start].pop)


# print(dfs_traverse(graph, 'A'))


def bfs_traverse(graph, start):
    queue = deque([start])
    return _traverse(graph, start, queue.popleft)


# print(bfs_traverse(graph, 'A'))


def dfs_traverse_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next_node in graph[start]:
        if next_node not in visited:
            dfs_traverse_recursive(graph, next_node, visited)
    return visited


# print(dfs_traverse_recursive(graph, 'A'))

# def find_path(graph, start, end, visited=[]):
    # # basecase
    # visitied = visited + [start]
    # if start == end:
        # return visited
    # if start not in graph:
        # return None
    # for node in graph[start]:
        # if node not in visited:
            # new_visited = find_path(graph, node, end, visited)
            # return new_visited
    # return None

# print(find_path(graph, 'A', 'F'))


if __name__ == "__main__":
    print("DFS:", sorted(dfs_traverse(graph, 'A')))
    print("BFS:", sorted(bfs_traverse(graph, 'A')))
    print("DFS Recursive:", sorted(dfs_traverse_recursive(graph, 'A')))