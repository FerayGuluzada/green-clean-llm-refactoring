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

    # Create a set of all literals to avoid duplicate lookups
    literals = set()
    for clause in formula:
        for lit, neg in clause:
            literals.add((lit, neg))
            literals.add((lit, not neg))

    # Initialize the graph with all literals
    for literal in literals:
        graph.setdefault(literal, [])

    # Build the implication graph
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        graph[(a_lit, a_neg)].append((b_lit, not b_neg))
        graph[(b_lit, b_neg)].append((a_lit, not a_neg))

    return graph


def dfs_transposed(graph, vertex, order, visited):
    visited.add(vertex)

    # Use a set to keep track of visited neighbors for faster lookup
    visited_neighbors = set()
    for neighbor in graph.get(vertex, []):
        if neighbor not in visited and neighbor not in visited_neighbors:
            dfs_transposed(graph, neighbor, order, visited)
            visited_neighbors.add(neighbor)

    order.append(vertex)


def dfs(graph, vertex, component, visited, vertex_scc):
    visited.add(vertex)
    vertex_scc[vertex] = component

    # Use a set to keep track of visited neighbors for faster lookup
    visited_neighbors = set()
    for neighbor in graph.get(vertex, []):
        if neighbor not in visited and neighbor not in visited_neighbors:
            dfs(graph, neighbor, component, visited, vertex_scc)
            visited_neighbors.add(neighbor)


def strongly_connected_components(graph):
    ''' Computes the strongly connected components of a graph '''
    order = []
    visited = set()

    # Create a transposed graph using a dictionary comprehension
    transposed_graph = {vertex: [] for vertex in graph}
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            transposed_graph.setdefault(neighbor, []).append(vertex)

    # Perform DFS on the transposed graph
    for vertex in graph:
        if vertex not in visited:
            dfs_transposed(transposed_graph, vertex, order, visited)

    visited = set()
    vertex_scc = {}
    component = 0

    # Perform DFS on the original graph in reverse order
    for vertex in reversed(order):
        if vertex not in visited:
            dfs(graph, vertex, component, visited, vertex_scc)
            component += 1

    return vertex_scc


def solve_sat(formula):
    graph = build_implication_graph(formula)
    vertex_scc = strongly_connected_components(graph)

    # Check for contradictions
    for (var, _) in graph:
        if vertex_scc.get((var, False)) == vertex_scc.get((var, True)):
            return None  # The formula is contradictory

    # Create a dictionary to store the component representatives
    component_repr = {component: next(vertex for vertex, comp in vertex_scc.items() if comp == component) for component in set(vertex_scc.values())}

    # Create a dictionary to store the component values
    component_value = {}
    for component in sorted(set(vertex_scc.values())):
        if component not in component_value:
            component_value[component] = False
            lit, neg = component_repr[component]
            component_value[vertex_scc.get((lit, not neg))] = True

    # Create a dictionary to store the variable assignments
    value = {var: component_value.get(vertex_scc.get((var, False))) for (var, _) in graph}

    return value


if __name__ == '__main__':
    result = solve_sat(formula)

    for (variable, assign) in result.items():
        print("{}:{}".format(variable, assign))