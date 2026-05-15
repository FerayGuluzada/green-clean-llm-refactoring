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
    vis[v] = True
    for u in graph.get(v, []):
        if not vis[u]:
            dfs_transposed(u, graph, order, vis)
    order.append(v)


def dfs(v, current_comp, vertex_scc, graph, vis):
    vis[v] = True
    vertex_scc[v] = current_comp
    for u in graph.get(v, []):
        if not vis[u]:
            dfs(u, current_comp, vertex_scc, graph, vis)


def scc(graph):
    ''' Computes the strongly connected components of a graph '''
    vertices = list(graph.keys())
    vis = {v: False for v in vertices}
    graph_transposed = {v: [] for v in vertices}
    
    # Build transposed graph
    for v in vertices:
        for u in graph.get(v, []):
            graph_transposed[u].append(v)
    
    # First DFS pass
    order = []
    for v in vertices:
        if not vis[v]:
            dfs_transposed(v, graph_transposed, order, vis)
    
    # Second DFS pass
    vis = {v: False for v in vertices}
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
    
    # Initialize all literals
    for clause in formula:
        for lit in clause:
            graph[lit] = []
            graph[(lit[0], not lit[1])] = []
    
    # Add implication edges
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        if (a_lit, a_neg) not in graph:
            graph[(a_lit, a_neg)] = []
        if (b_lit, not b_neg) not in graph:
            graph[(b_lit, not b_neg)] = []
        graph[(a_lit, a_neg)].append((b_lit, not b_neg))
        
        if (b_lit, b_neg) not in graph:
            graph[(b_lit, b_neg)] = []
        if (a_lit, not a_neg) not in graph:
            graph[(a_lit, not a_neg)] = []
        graph[(b_lit, b_neg)].append((a_lit, not a_neg))
    
    return graph


def solve_sat(formula):
    graph = build_graph(formula)
    vertex_scc = scc(graph)

    # Check for contradictions
    for var, _ in list(graph.keys()):
        if vertex_scc.get((var, False)) == vertex_scc.get((var, True)):
            return None

    # Assign values to components
    comp_repr = {}
    for vertex, comp in vertex_scc.items():
        if comp not in comp_repr:
            comp_repr[comp] = vertex

    comp_value = {}
    components = sorted(set(vertex_scc.values()))

    for comp in components:
        if comp not in comp_value:
            lit, neg = comp_repr[comp]
            comp_value[comp] = False
            comp_value[vertex_scc[(lit, not neg)]] = True

    return {var: comp_value[vertex_scc[(var, False)]] 
            for var, _ in graph.keys() if (var, False) in vertex_scc}


if __name__ == '__main__':
    result = solve_sat(formula)
    if result:
        for variable, assign in result.items():
            print("{}:{}".format(variable, assign))
    else:
        print("No solution")