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


def build_transposed_graph(graph):
    ''' Builds the transposed graph '''
    transposed_graph = {vertex: [] for vertex in graph}
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            transposed_graph[neighbor].append(vertex)
    return transposed_graph


def dfs(graph, vertex, visited, order):
    ''' Performs a depth-first search on the graph '''
    visited[vertex] = True
    for neighbor in graph[vertex]:
        if not visited[neighbor]:
            dfs(graph, neighbor, visited, order)
    order.append(vertex)


def dfs_scc(graph, vertex, visited, scc, current_comp):
    ''' Performs a depth-first search to find strongly connected components '''
    visited[vertex] = True
    scc[vertex] = current_comp
    for neighbor in graph[vertex]:
        if not visited[neighbor]:
            dfs_scc(graph, neighbor, visited, scc, current_comp)


def build_implication_graph(formula):
    ''' Builds the implication graph from the formula '''
    graph = {}
    for clause in formula:
        for lit, neg in [(lit, neg) for lit, neg in clause]:
            graph[(lit, neg)] = []
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        graph[(a_lit, a_neg)].append((b_lit, not b_neg))
        graph[(b_lit, b_neg)].append((a_lit, not a_neg))
    return graph


def find_strongly_connected_components(graph):
    ''' Finds strongly connected components in the graph '''
    order = []
    visited = {vertex: False for vertex in graph}
    for vertex in graph:
        if not visited[vertex]:
            dfs(build_transposed_graph(graph), vertex, visited, order)
    visited = {vertex: False for vertex in graph}
    scc = {}
    current_comp = 0
    for vertex in reversed(order):
        if not visited[vertex]:
            dfs_scc(graph, vertex, visited, scc, current_comp)
            current_comp += 1
    return scc


def solve_2_sat(formula):
    ''' Solves the 2-SAT problem '''
    graph = build_implication_graph(formula)
    scc = find_strongly_connected_components(graph)
    for var, neg in graph:
        if scc[(var, False)] == scc[(var, True)]:
            return None  # The formula is contradictory
    comp_repr = {comp: vertex for vertex, comp in scc.items() if vertex[1] == False}
    comp_value = {comp: False for comp in comp_repr}
    for comp, vertex in comp_repr.items():
        comp_value[scc[(vertex[0], not vertex[1])]] = True
    value = {var: comp_value[scc[(var, False)]] for var, neg in graph if neg == False}
    return value


if __name__ == '__main__':
    result = solve_2_sat(formula)
    for variable, assign in result.items():
        print(f"{variable}: {assign}")