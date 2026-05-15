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


def add_edge(graph, vertex_from, vertex_to):
    graph[vertex_from].append(vertex_to)


def reverse_literal(literal):
    name, is_neg = literal
    return name, not is_neg


def dfs_postorder(start_vertex, graph, visited, order):
    stack = [(start_vertex, False)]

    while stack:
        vertex, expanded = stack.pop()
        if expanded:
            order.append(vertex)
            continue

        if vertex in visited:
            continue

        visited.add(vertex)
        stack.append((vertex, True))

        for neighbour in graph[vertex]:
            if neighbour not in visited:
                stack.append((neighbour, False))


def dfs_assign_component(start_vertex, component_id, graph, visited, vertex_scc):
    stack = [start_vertex]
    visited.add(start_vertex)

    while stack:
        vertex = stack.pop()
        vertex_scc[vertex] = component_id

        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(neighbour)


def scc(graph, transposed):
    ''' Computes the strongly connected components of a graph '''
    order = []
    visited = set()

    for vertex in graph:
        if vertex not in visited:
            dfs_postorder(vertex, transposed, visited, order)

    visited.clear()
    vertex_scc = {}
    component_id = 0

    for vertex in reversed(order):
        if vertex not in visited:
            # Each dfs will visit exactly one component
            dfs_assign_component(vertex, component_id, graph, visited, vertex_scc)
            component_id += 1

    return vertex_scc


def build_graph(formula):
    ''' Builds the implication graph from the formula '''
    graph = {}
    transposed = {}
    variables = set()

    for left, right in formula:
        left_name, _ = left
        right_name, _ = right
        variables.add(left_name)
        variables.add(right_name)

    for name in variables:
        positive = (name, False)
        negative = (name, True)
        graph[positive] = []
        graph[negative] = []
        transposed[positive] = []
        transposed[negative] = []

    for left, right in formula:
        not_left = reverse_literal(left)
        not_right = reverse_literal(right)

        add_edge(graph, not_left, right)
        add_edge(transposed, right, not_left)

        add_edge(graph, not_right, left)
        add_edge(transposed, left, not_right)

    return graph, transposed, variables


def solve_sat(formula):
    graph, transposed, variables = build_graph(formula)
    vertex_scc = scc(graph, transposed)

    assignment = {}
    for variable in variables:
        false_literal = (variable, False)
        true_literal = (variable, True)

        false_component = vertex_scc[false_literal]
        true_component = vertex_scc[true_literal]

        if false_component == true_component:
            return None  # The formula is contradictory

        assignment[variable] = false_component < true_component

    return assignment


if __name__ == '__main__':
    result = solve_sat(formula)

    for (variable, assign) in result.items():
        print("{}:{}".format(variable, assign))