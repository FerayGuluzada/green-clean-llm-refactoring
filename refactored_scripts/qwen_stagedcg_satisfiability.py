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
    stack = [v]
    
    while stack:
        node = stack.pop()
        # Re-visit node to append to order after processing children
        if node is not None:
            for u in graph.get(node, []):
                if not vis[u]:
                    vis[u] = True
                    stack.append(u)
            order.append(node)
        else:
            order.append(stack.pop())


def dfs(v, current_comp, vertex_scc, graph, vis):
    vis[v] = True
    stack = [v]
    
    while stack:
        node = stack.pop()
        vertex_scc[node] = current_comp
        for u in graph.get(node, []):
            if not vis[u]:
                vis[u] = True
                stack.append(u)


def add_edge(graph, vertex_from, vertex_to):
    if vertex_from in graph:
        graph[vertex_from].append(vertex_to)
    else:
        graph[vertex_from] = [vertex_to]


def build_transposed_graph(graph):
    transposed = {vertex: [] for vertex in graph}
    for v, neighbors in graph.items():
        for u in neighbors:
            transposed[u].append(v)
    return transposed


def scc(graph):
    ''' Computes the strongly connected components of a graph '''
    vis = {vertex: False for vertex in graph}
    transposed = build_transposed_graph(graph)
    
    order = []
    for v in graph:
        if not vis[v]:
            dfs_transposed(v, transposed, order, vis)
    
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
    
    # Add implication edges and initialize vertices
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        # Ensure all four literals exist in graph
        literals = [(a_lit, a_neg), (a_lit, not a_neg), (b_lit, b_neg), (b_lit, not b_neg)]
        for lit in literals:
            if lit not in graph:
                graph[lit] = []
        
        # Add implication edges
        graph[(a_lit, a_neg)].append((b_lit, not b_neg))
        graph[(b_lit, b_neg)].append((a_lit, not a_neg))
    
    return graph


def solve_sat(formula):
    graph = build_graph(formula)
    vertex_scc = scc(graph)
    
    # Check for contradictions
    for var, _ in graph:
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None
    
    # Assign values to components
    comp_repr = {}
    for vertex in graph:
        comp = vertex_scc[vertex]
        if comp not in comp_repr:
            comp_repr[comp] = vertex
    
    comp_value = {}
    components = set(vertex_scc.values())
    
    for comp in components:
        if comp not in comp_value:
            comp_value[comp] = False
            lit, neg = comp_repr[comp]
            comp_value[vertex_scc[(lit, not neg)]] = True
    
    # Map variable assignments
    return {var: comp_value[vertex_scc[(var, False)]] for var, _ in graph}


if __name__ == '__main__':
    result = solve_sat(formula)
    if result:
        for variable, assign in result.items():
            print("{}:{}".format(variable, assign))