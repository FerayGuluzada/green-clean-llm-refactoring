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


def _traverse_dfs(graph, start):
    visited = set()
    pending = [start]
    pending_pop = pending.pop
    pending_extend = pending.extend
    visited_add = visited.add

    while pending:
        node = pending_pop()
        if node in visited:
            continue

        visited_add(node)
        pending_extend(neighbor for neighbor in graph[node] if neighbor not in visited)

    return visited


def _traverse_bfs(graph, start):
    visited = {start}
    pending = [start]
    index = 0
    pending_append = pending.append
    visited_add = visited.add

    while index < len(pending):
        node = pending[index]
        index += 1

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited_add(neighbor)
                pending_append(neighbor)

    return visited


def dfs_traverse(graph, start):
    return _traverse_dfs(graph, start)


def bfs_traverse(graph, start):
    return _traverse_bfs(graph, start)


def dfs_traverse_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)
    for next_node in graph[start]:
        if next_node not in visited:
            dfs_traverse_recursive(graph, next_node, visited)

    return visited


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