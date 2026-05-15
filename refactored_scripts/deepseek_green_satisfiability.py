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


def dfs_transposed(v, graph, order, vis):
    stack = [v]
    while stack:
        v = stack[-1]
        if not vis[v]:
            vis[v] = True
            for u in graph[v]:
                if not vis[u]:
                    stack.append(u)
            continue
        stack.pop()
        order.append(v)


def dfs(v, current_comp, vertex_scc, graph, vis):
    stack = [v]
    while stack:
        v = stack.pop()
        if vis[v]:
            continue
        vis[v] = True
        vertex_scc[v] = current_comp
        for u in graph[v]:
            if not vis[u]:
                stack.append(u)


def add_edge(graph, vertex_from, vertex_to):
    if vertex_from not in graph:
        graph[vertex_from] = []
    graph[vertex_from].append(vertex_to)


def scc(graph):
    ''' Computes the strongly connected components of a graph '''
    order = []
    vis = {vertex: False for vertex in graph}
    graph_transposed = {vertex: [] for vertex in graph}

    # Build transposed graph and compute finishing times
    for v, neighbours in graph.items():
        for u in neighbours:
            if u not in graph_transposed:
                graph_transposed[u] = []
            graph_transposed[u].append(v)

    for v in graph:
        if not vis[v]:
            dfs_transposed(v, graph_transposed, order, vis)

    vis = {vertex: False for vertex in graph}
    vertex_scc = {}
    current_comp = 0

    for v in reversed(order):
        if not vis[v]:
            dfs(v, current_comp, vertex_scc, graph, vis)
            current_comp += 1

    return vertex_scc


def build_graph(formula):
    ''' Builds the implication graph from the formula '''
    graph = {}
    variables = set()

    # Collect all variables first
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        variables.add(a_lit)
        variables.add(b_lit)

    # Initialize graph with all possible literals
    for var in variables:
        graph[(var, False)] = []
        graph[(var, True)] = []

    # Add edges
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        graph[(a_lit, a_neg)].append((b_lit, not b_neg))
        graph[(b_lit, b_neg)].append((a_lit, not a_neg))

    return graph


def solve_sat(formula):
    if not formula:
        return {}

    graph = build_graph(formula)
    vertex_scc = scc(graph)

    # Check for contradictions
    for var in {v[0] for v in graph}:
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None

    # Process components in topological order
    comp_repr = {}
    for vertex, comp in vertex_scc.items():
        if comp not in comp_repr:
            comp_repr[comp] = vertex

    comp_value = {}
    components = set(vertex_scc.values())

    for comp in components:
        if comp not in comp_value:
            comp_value[comp] = False
            lit, neg = comp_repr[comp]
            comp_value[vertex_scc[(lit, not neg)]] = True

    # Build assignment
    value = {}
    for var in {v[0] for v in graph}:
        value[var] = comp_value[vertex_scc[(var, False)]]

    return value


if __name__ == '__main__':
    result = solve_sat(formula)

    for (variable, assign) in result.items():
        print("{}:{}".format(variable, assign))