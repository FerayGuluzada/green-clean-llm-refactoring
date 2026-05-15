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


def scc(graph):
    ''' Computes the strongly connected components of a graph '''
    order = []
    vis = set()

    graph_transposed = {vertex: [] for vertex in graph}
    for v, neighbours in graph.items():
        for u in neighbours:
            graph_transposed[u].append(v)

    for start in graph:
        if start in vis:
            continue

        stack = [(start, 0)]
        vis.add(start)

        while stack:
            v, idx = stack[-1]
            neighbours = graph_transposed[v]

            if idx < len(neighbours):
                u = neighbours[idx]
                stack[-1] = (v, idx + 1)
                if u not in vis:
                    vis.add(u)
                    stack.append((u, 0))
            else:
                order.append(v)
                stack.pop()

    vis.clear()
    vertex_scc = {}
    current_comp = 0

    for start in reversed(order):
        if start in vis:
            continue

        stack = [start]
        vis.add(start)
        vertex_scc[start] = current_comp

        while stack:
            v = stack.pop()
            for u in graph[v]:
                if u not in vis:
                    vis.add(u)
                    vertex_scc[u] = current_comp
                    stack.append(u)

        current_comp += 1

    return vertex_scc


def build_graph(formula):
    ''' Builds the implication graph from the formula '''
    variables = set()
    for (a_lit, _), (b_lit, _) in formula:
        variables.add(a_lit)
        variables.add(b_lit)

    graph = {}
    for lit in variables:
        graph[(lit, False)] = []
        graph[(lit, True)] = []

    for ((a_lit, a_neg), (b_lit, b_neg)) in formula:
        add_edge(graph, (a_lit, a_neg), (b_lit, not b_neg))
        add_edge(graph, (b_lit, b_neg), (a_lit, not a_neg))

    return graph, variables


def solve_sat(formula):
    graph, variables = build_graph(formula)
    vertex_scc = scc(graph)

    for var in variables:
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None  # The formula is contradictory

    comp_repr = {}  # An arbitrary representant from each component
    for vertex, comp in vertex_scc.items():
        if comp not in comp_repr:
            comp_repr[comp] = vertex

    comp_value = {}  # True/False value for each strongly connected component
    for comp in sorted(comp_repr):
        if comp not in comp_value:
            comp_value[comp] = False
            lit, neg = comp_repr[comp]
            comp_value[vertex_scc[(lit, not neg)]] = True

    return {var: comp_value[vertex_scc[(var, False)]] for var in variables}


if __name__ == '__main__':
    result = solve_sat(formula)

    for (variable, assign) in result.items():
        print("{}:{}".format(variable, assign))