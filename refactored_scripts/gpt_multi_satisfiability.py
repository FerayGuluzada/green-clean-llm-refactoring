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


def dfs_order(start, graph, vis, order):
    stack = [(start, False)]
    while stack:
        vertex, expanded = stack.pop()
        if expanded:
            order.append(vertex)
            continue
        if vis[vertex]:
            continue
        vis[vertex] = True
        stack.append((vertex, True))
        for neighbour in graph[vertex]:
            if not vis[neighbour]:
                stack.append((neighbour, False))


def dfs_component(start, graph, vis, vertex_scc, component_id):
    stack = [start]
    vis[start] = True
    while stack:
        vertex = stack.pop()
        vertex_scc[vertex] = component_id
        for neighbour in graph[vertex]:
            if not vis[neighbour]:
                vis[neighbour] = True
                stack.append(neighbour)


def scc(graph):
    ''' Computes the strongly connected components of a graph '''
    transposed = {vertex: [] for vertex in graph}
    for vertex, neighbours in graph.items():
        for neighbour in neighbours:
            transposed[neighbour].append(vertex)

    order = []
    vis = {vertex: False for vertex in graph}
    for vertex in graph:
        if not vis[vertex]:
            dfs_order(vertex, transposed, vis, order)

    vis = {vertex: False for vertex in graph}
    vertex_scc = {}
    component_id = 0
    for vertex in reversed(order):
        if not vis[vertex]:
            dfs_component(vertex, graph, vis, vertex_scc, component_id)
            component_id += 1

    return vertex_scc


def build_graph(formula):
    ''' Builds the implication graph from the formula '''
    variables = set()
    for (left, right) in formula:
        variables.add(left[0])
        variables.add(right[0])

    graph = {(var, neg): [] for var in variables for neg in (False, True)}

    for (a_var, a_neg), (b_var, b_neg) in formula:
        add_edge(graph, (a_var, not a_neg), (b_var, b_neg))
        add_edge(graph, (b_var, not b_neg), (a_var, a_neg))

    return graph


def solve_sat(formula):
    graph = build_graph(formula)
    vertex_scc = scc(graph)

    variables = {var for var, _ in graph}
    for var in variables:
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None  # The formula is contradictory

    return {
        var: vertex_scc[(var, False)] > vertex_scc[(var, True)]
        for var in variables
    }


if __name__ == '__main__':
    result = solve_sat(formula)

    for (variable, assign) in result.items():
        print("{}:{}".format(variable, assign))