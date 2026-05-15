graph = {'A': set(['B', 'C', 'F']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['A', 'C', 'E'])}

# dfs and bfs are the ultimately same except that they are visiting nodes in
# different order. To simulate this ordering we would use stack for dfs and
# queue for bfs.
#

def dfs_traverse(graph, start):
    visited = {start}
    stack = [start]
    get_neighbors = graph.get
    add_visited = visited.add
    pop_stack = stack.pop
    append_stack = stack.append

    while stack:
        node = pop_stack()
        for nextNode in get_neighbors(node, ()):
            if nextNode not in visited:
                add_visited(nextNode)
                append_stack(nextNode)
    return visited

# print(dfs_traverse(graph, 'A'))


def bfs_traverse(graph, start):
    visited = {start}
    queue = [start]
    index = 0
    get_neighbors = graph.get
    add_visited = visited.add
    append_queue = queue.append

    while index < len(queue):
        node = queue[index]
        index += 1
        for nextNode in get_neighbors(node, ()):
            if nextNode not in visited:
                add_visited(nextNode)
                append_queue(nextNode)
    return visited

# print(bfs_traverse(graph, 'A'))

def dfs_traverse_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for nextNode in graph[start]:
        if nextNode not in visited:
            dfs_traverse_recursive(graph, nextNode, visited)
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