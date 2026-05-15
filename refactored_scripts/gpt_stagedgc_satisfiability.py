'''
Given a formula in conjunctive normal form (2-CNF), finds a way to assign
True/False values to all variables to satisfy all clauses, or reports there
is no solution.

https://en.wikipedia.org/wiki/2-satisfiability
'''


''' Format:
        - each clause is a pair of literals
        - each literal in the form (name, is_neg)
          where name is an arbitrary identifier,
          and is_neg is true if the literal is negated
'''
formula = [(('x', False), ('y', False)),
           (('y', True), ('y', True)),
           (('a', False), ('b', False)),
           (('a', True), ('c', True)),
           (('c', False), ('b', True))]


def negate(literal):
    name, is_neg = literal
    return name, not is_neg


def dfs_finish_order(start, graph, visited, order):
    stack = [(start, 0)]
    visited[start] = True

    while stack:
        vertex, next_index = stack[-1]
        neighbours = graph[vertex]

        if next_index < len(neighbours):
            neighbour = neighbours[next_index]
            stack[-1] = (vertex, next_index + 1)
            if not visited[neighbour]:
                visited[neighbour] = True
                stack.append((neighbour, 0))
            continue

        order.append(vertex)
        stack.pop()


def dfs_assign_component(start, component_id, vertex_scc, graph, visited):
    stack = [start]
    visited[start] = True
    vertex_scc[start] = component_id

    while stack:
        vertex = stack.pop()
        for neighbour in graph[vertex]:
            if visited[neighbour]:
                continue
            visited[neighbour] = True
            vertex_scc[neighbour] = component_id
            stack.append(neighbour)


def transpose_graph(graph):
    transposed = {vertex: [] for vertex in graph}
    for vertex, neighbours in graph.items():
        for neighbour in neighbours:
            transposed[neighbour].append(vertex)
    return transposed


def scc(graph):
    ''' Computes the strongly connected components of a graph '''
    order = []
    visited = {vertex: False for vertex in graph}
    transposed = transpose_graph(graph)

    for vertex in graph:
        if not visited[vertex]:
            dfs_finish_order(vertex, transposed, visited, order)

    visited = {vertex: False for vertex in graph}
    vertex_scc = {}

    component_id = 0
    for vertex in reversed(order):
        if visited[vertex]:
            continue
        # Each dfs will visit exactly one component
        dfs_assign_component(vertex, component_id, vertex_scc, graph, visited)
        component_id += 1

    return vertex_scc


def build_graph(formula):
    ''' Builds the implication graph from the formula '''
    variables = {name for clause in formula for name, _ in clause}

    graph = {}
    for variable in variables:
        graph[(variable, False)] = []
        graph[(variable, True)] = []

    for left_literal, right_literal in formula:
        graph[negate(left_literal)].append(right_literal)
        graph[negate(right_literal)].append(left_literal)

    return graph, variables


def solve_sat(formula):
    graph, variables = build_graph(formula)
    vertex_scc = scc(graph)

    for variable in variables:
        if vertex_scc[(variable, False)] == vertex_scc[(variable, True)]:
            return None  # The formula is contradictory

    return {
        variable: vertex_scc[(variable, False)] < vertex_scc[(variable, True)]
        for variable in variables
    }


if __name__ == '__main__':
    result = solve_sat(formula)

    for variable, assign in result.items():
        print("{}:{}".format(variable, assign))