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


def dfs_postorder(vertex, graph, visited, order):
    visited[vertex] = True
    for neighbour in graph[vertex]:
        if not visited[neighbour]:
            dfs_postorder(neighbour, graph, visited, order)
    order.append(vertex)


def dfs_assign_component(vertex, component_id, graph, visited, vertex_scc):
    visited[vertex] = True
    vertex_scc[vertex] = component_id
    for neighbour in graph[vertex]:
        if not visited[neighbour]:
            dfs_assign_component(neighbour, component_id, graph, visited, vertex_scc)


def add_edge(graph, source, target):
    graph.setdefault(source, []).append(target)


def transpose_graph(graph):
    transposed = {vertex: [] for vertex in graph}
    for source, neighbours in graph.items():
        for target in neighbours:
            add_edge(transposed, target, source)
    return transposed


def scc(graph):
    ''' Computes the strongly connected components of a graph '''
    order = []
    visited = {vertex: False for vertex in graph}
    transposed = transpose_graph(graph)

    for vertex in graph:
        if not visited[vertex]:
            dfs_postorder(vertex, transposed, visited, order)

    visited = {vertex: False for vertex in graph}
    vertex_scc = {}
    component_id = 0

    for vertex in reversed(order):
        if not visited[vertex]:
            # Each dfs will visit exactly one component
            dfs_assign_component(vertex, component_id, graph, visited, vertex_scc)
            component_id += 1

    return vertex_scc


def literal_vertex(name, is_negated):
    return name, is_negated


def opposite_literal(literal):
    name, is_negated = literal
    return name, not is_negated


def build_graph(formula):
    ''' Builds the implication graph from the formula '''
    graph = {}
    variables = {name for clause in formula for (name, _) in clause}

    for name in variables:
        graph[literal_vertex(name, False)] = []
        graph[literal_vertex(name, True)] = []

    for left_literal, right_literal in formula:
        add_edge(graph, opposite_literal(left_literal), right_literal)
        add_edge(graph, opposite_literal(right_literal), left_literal)

    return graph


def solve_sat(formula):
    graph = build_graph(formula)
    vertex_scc = scc(graph)
    variables = {name for name, _ in graph}

    for var in variables:
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None  # The formula is contradictory

    component_repr = {}
    for vertex, component_id in vertex_scc.items():
        component_repr.setdefault(component_id, vertex)

    component_value = {}
    for component_id in sorted(set(vertex_scc.values())):
        if component_id in component_value:
            continue

        component_value[component_id] = False
        representative = component_repr[component_id]
        opposite_component = vertex_scc[opposite_literal(representative)]
        component_value[opposite_component] = True

    return {var: component_value[vertex_scc[(var, False)]] for var in variables}


if __name__ == '__main__':
    result = solve_sat(formula)

    for (variable, assign) in result.items():
        print("{}:{}".format(variable, assign))