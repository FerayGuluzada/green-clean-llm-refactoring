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


def dfs_transposed(vertex, graph, order, visited):
    visited[vertex] = True

    for neighbor in graph.get(vertex, []):
        if not visited[neighbor]:
            dfs_transposed(neighbor, graph, order, visited)

    order.append(vertex)


def dfs(vertex, component_id, vertex_scc, graph, visited):
    visited[vertex] = True
    vertex_scc[vertex] = component_id

    for neighbor in graph.get(vertex, []):
        if not visited[neighbor]:
            dfs(neighbor, component_id, vertex_scc, graph, visited)


def build_implication_graph(clauses):
    ''' Builds the implication graph from the formula '''
    graph = {}
    
    # Initialize all literals in the graph
    for (lit1, _), (lit2, _) in clauses:
        for lit in [lit1, lit2]:
            for polarity in [False, True]:
                graph[(lit, polarity)] = []
    
    # Add implication edges
    for (a_lit, a_neg), (b_lit, b_neg) in clauses:
        # (a OR b) is equivalent to (NOT a -> b) AND (NOT b -> a)
        graph.setdefault((a_lit, a_neg), []).append((b_lit, not b_neg))
        graph.setdefault((b_lit, b_neg), []).append((a_lit, not a_neg))
    
    return graph


def kosaraju(graph):
    ''' Computes the strongly connected components of a graph using Kosaraju's algorithm '''
    # First DFS on transposed graph to get finishing order
    visited = {vertex: False for vertex in graph}
    finish_order = []
    
    transposed = {vertex: [] for vertex in graph}
    for v in graph:
        for u in graph[v]:
            transposed[u].append(v)
    
    for vertex in graph:
        if not visited[vertex]:
            dfs_transposed(vertex, transposed, finish_order, visited)
    
    # Second DFS in reverse finish order to find SCCs
    visited = {vertex: False for vertex in graph}
    vertex_scc = {}
    component_id = 0
    
    for vertex in reversed(finish_order):
        if not visited[vertex]:
            dfs(vertex, component_id, vertex_scc, graph, visited)
            component_id += 1
    
    return vertex_scc


def solve_2sat(clauses):
    ''' Solves 2-SAT problem using SCC-based approach '''
    # Build implication graph and compute SCCs
    graph = build_implication_graph(clauses)
    vertex_scc = kosaraju(graph)
    
    # Check for contradictions (variable and its negation in same SCC)
    for (var, _) in graph:
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None  # Unsatisfiable
    
    # Assign truth values based on SCC topological order
    # SCCs with lower IDs come before those with higher IDs in topological sort
    scc_to_value = {}
    result = {}
    
    # For each variable, assign value based on which SCC has smaller ID
    for (var, _) in graph:
        false_scc = vertex_scc[(var, False)]
        true_scc = vertex_scc[(var, True)]
        
        if false_scc not in scc_to_value:
            scc_to_value[false_scc] = False
        if true_scc not in scc_to_value:
            scc_to_value[true_scc] = False
            
        # If the SCC containing (var, True) has a smaller ID than 
        # the one containing (var, False), then var should be True
        result[var] = false_scc > true_scc
    
    return result


if __name__ == '__main__':
    result = solve_2sat(formula)
    
    if result is None:
        print("No solution")
    else:
        for variable, assignment in result.items():
            print("{}:{}".format(variable, assignment))