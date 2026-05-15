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


def _dfs_transposed(v, graph, order, visited):
    visited[v] = True
    
    for u in graph[v]:
        if not visited[u]:
            _dfs_transposed(u, graph, order, visited)
    
    order.append(v)


def _dfs(v, comp_id, vertex_scc, graph, visited):
    visited[v] = True
    vertex_scc[v] = comp_id
    
    for u in graph[v]:
        if not visited[u]:
            _dfs(u, comp_id, vertex_scc, graph, visited)


def _add_edge(graph, from_v, to_v):
    graph.setdefault(from_v, []).append(to_v)


def _build_graph(formula):
    ''' Builds the implication graph from the formula '''
    graph = {}
    
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        for lit, neg in [(a_lit, a_neg), (b_lit, b_neg)]:
            for neg_state in (False, True):
                graph[(lit, neg_state)] = []
    
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        _add_edge(graph, (a_lit, a_neg), (b_lit, not b_neg))
        _add_edge(graph, (b_lit, b_neg), (a_lit, not a_neg))
    
    return graph


def _compute_scc(graph):
    ''' Computes the strongly connected components of a graph '''
    order = []
    visited = {v: False for v in graph}
    
    transposed = {v: [] for v in graph}
    for v, neighbors in graph.items():
        for u in neighbors:
            _add_edge(transposed, u, v)
    
    for v in graph:
        if not visited[v]:
            _dfs_transposed(v, transposed, order, visited)
    
    visited = {v: False for v in graph}
    vertex_scc = {}
    comp_id = 0
    
    for v in reversed(order):
        if not visited[v]:
            _dfs(v, comp_id, vertex_scc, graph, visited)
            comp_id += 1
    
    return vertex_scc


def _extract_assignment(graph, vertex_scc):
    ''' Extracts variable assignment from SCC results '''
    for var, _ in graph:
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None
    
    comp_repr = {}
    for vertex, comp in vertex_scc.items():
        if comp not in comp_repr:
            comp_repr[comp] = vertex
    
    comp_value = {}
    for comp in sorted(set(vertex_scc.values())):
        if comp not in comp_value:
            comp_value[comp] = False
            lit, neg = comp_repr[comp]
            comp_value[vertex_scc[(lit, not neg)]] = True
    
    return {var: comp_value[vertex_scc[(var, False)]] for var, _ in graph}


def solve_sat(formula):
    ''' Solves 2-SAT problem using implication graph and SCC '''
    graph = _build_graph(formula)
    vertex_scc = _compute_scc(graph)
    return _extract_assignment(graph, vertex_scc)


if __name__ == '__main__':
    result = solve_sat(formula)
    
    for variable, assign in result.items():
        print(f"{variable}:{assign}")