'''
Given a formula in conjunctive normal form (2-CNF), finds a way to assign
True/False values to all variables to satisfy all clauses, or reports there
is no solution.

https://en.wikipedia.org/wiki/2-satisfiability
'''

# Format:
# - each clause is a pair of literals
# - each literal in the form (name, is_neg)
#   where name is an arbitrary identifier,
#   and is_neg is true if the literal is negated
formula = [(('x', False), ('y', False)),
           (('y', True), ('y', True)),
           (('a', False), ('b', False)),
           (('a', True), ('c', True)),
           (('c', False), ('b', True))]


def build_implication_graph(formula):
    ''' Builds the implication graph from the formula '''
    graph = {}

    for clause in formula:
        for (lit, neg) in clause:
            for neg_val in [False, True]:
                graph.setdefault((lit, neg_val), [])

    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        graph[(a_lit, a_neg)].append((b_lit, not b_neg))
        graph[(b_lit, b_neg)].append((a_lit, not a_neg))

    return graph


def dfs_transposed(graph, vertex, order, visited):
    visited.add(vertex)

    for neighbor in graph.get(vertex, []):
        if neighbor not in visited:
            dfs_transposed(graph, neighbor, order, visited)

    order.append(vertex)


def dfs(graph, vertex, component, visited, vertex_scc):
    visited.add(vertex)
    vertex_scc[vertex] = component

    for neighbor in graph.get(vertex, []):
        if neighbor not in visited:
            dfs(graph, neighbor, component, visited, vertex_scc)


def strongly_connected_components(graph):
    ''' Computes the strongly connected components of a graph '''
    order = []
    visited = set()

    transposed_graph = {}
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            transposed_graph.setdefault(neighbor, []).append(vertex)

    for vertex in graph:
        if vertex not in visited:
            dfs_transposed(transposed_graph, vertex, order, visited)

    visited = set()
    vertex_scc = {}
    component = 0

    for vertex in reversed(order):
        if vertex not in visited:
            dfs(graph, vertex, component, visited, vertex_scc)
            component += 1

    return vertex_scc


def solve_sat(formula):
    graph = build_implication_graph(formula)
    vertex_scc = strongly_connected_components(graph)

    for (var, _) in graph:
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None  # The formula is contradictory

    component_repr = {}
    for vertex in graph:
        if vertex_scc[vertex] not in component_repr:
            component_repr[vertex_scc[vertex]] = vertex

    component_value = {}
    components = sorted(vertex_scc.values())

    for component in components:
        if component not in component_value:
            component_value[component] = False

            lit, neg = component_repr[component]
            component_value[vertex_scc[(lit, not neg)]] = True

    value = {var: component_value[vertex_scc[(var, False)]] for var, _ in graph}

    return value


if __name__ == '__main__':
    result = solve_sat(formula)

    for (variable, assign) in result.items():
        print("{}:{}".format(variable, assign))