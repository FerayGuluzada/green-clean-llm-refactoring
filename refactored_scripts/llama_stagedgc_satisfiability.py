"""
Given a formula in conjunctive normal form (2-CNF), finds a way to assign
True/False values to all variables to satisfy all clauses, or reports there
is no solution.

https://en.wikipedia.org/wiki/2-satisfiability
"""

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


class Graph:
    """Represents a directed graph."""
    def __init__(self):
        self.vertices = set()
        self.edges = {}

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        self.vertices.add(vertex)
        if vertex not in self.edges:
            self.edges[vertex] = []

    def add_edge(self, vertex_from, vertex_to):
        """Add an edge to the graph."""
        self.edges[vertex_from].append(vertex_to)


def build_transposed_graph(graph):
    """Build the transposed graph."""
    transposed_graph = Graph()
    for vertex in graph.vertices:
        transposed_graph.add_vertex(vertex)
    for vertex, neighbours in graph.edges.items():
        for neighbour in neighbours:
            transposed_graph.add_edge(neighbour, vertex)
    return transposed_graph


def dfs_transposed(graph, vertex, order, visited):
    """Depth-first search on the transposed graph."""
    visited.add(vertex)
    for neighbour in graph.edges.get(vertex, []):
        if neighbour not in visited:
            dfs_transposed(graph, neighbour, order, visited)
    order.append(vertex)


def dfs(graph, vertex, current_comp, vertex_scc, visited):
    """Depth-first search on the original graph."""
    visited.add(vertex)
    vertex_scc[vertex] = current_comp
    for neighbour in graph.edges.get(vertex, []):
        if neighbour not in visited:
            dfs(graph, neighbour, current_comp, vertex_scc, visited)


def compute_scc(graph):
    """Compute the strongly connected components of a graph."""
    order = []
    visited = set()
    transposed_graph = build_transposed_graph(graph)
    for vertex in graph.vertices:
        if vertex not in visited:
            dfs_transposed(transposed_graph, vertex, order, visited)

    visited = set()
    vertex_scc = {}
    current_comp = 0
    for vertex in reversed(order):
        if vertex not in visited:
            dfs(graph, vertex, current_comp, vertex_scc, visited)
            current_comp += 1

    return vertex_scc


def build_implication_graph(formula):
    """Build the implication graph from the formula."""
    graph = Graph()
    vertices = set()

    for clause in formula:
        for lit, _ in clause:
            for neg in [False, True]:
                vertices.add((lit, neg))

    for vertex in vertices:
        graph.add_vertex(vertex)

    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        graph.add_edge((a_lit, a_neg), (b_lit, not b_neg))
        graph.add_edge((b_lit, b_neg), (a_lit, not a_neg))

    return graph


def solve_sat(formula):
    """Solve the 2-SAT problem."""
    graph = build_implication_graph(formula)
    vertex_scc = compute_scc(graph)

    for (var, _) in graph.vertices:
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None  # The formula is contradictory

    comp_repr = {}
    for vertex in graph.vertices:
        if vertex_scc[vertex] not in comp_repr:
            comp_repr[vertex_scc[vertex]] = vertex

    comp_value = {}
    components = sorted(vertex_scc.values())

    for comp in components:
        if comp not in comp_value:
            comp_value[comp] = False
            lit, neg = comp_repr[comp]
            comp_value[vertex_scc[(lit, not neg)]] = True

    value = {var: comp_value[vertex_scc[(var, False)]] for var, _ in graph.vertices}

    return value


if __name__ == '__main__':
    result = solve_sat(formula)
    for (variable, assign) in result.items():
        print("{}:{}".format(variable, assign))