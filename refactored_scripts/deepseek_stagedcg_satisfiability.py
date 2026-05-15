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
    '''DFS on transposed graph for topological ordering'''
    stack = [v]
    
    while stack:
        current = stack[-1]
        
        if not visited[current]:
            visited[current] = True
            
            for u in graph[current]:
                if not visited[u]:
                    stack.append(u)
                    break
            else:
                stack.pop()
                order.append(current)
        else:
            stack.pop()


def _dfs(v, comp_id, vertex_scc, graph, visited):
    '''DFS for SCC assignment using iterative approach'''
    stack = [v]
    
    while stack:
        current = stack.pop()
        
        if visited[current]:
            continue
            
        visited[current] = True
        vertex_scc[current] = comp_id
        
        for u in graph[current]:
            if not visited[u]:
                stack.append(u)


def _add_edge(graph, from_v, to_v):
    '''Adds edge to adjacency list with pre-allocation'''
    if from_v not in graph:
        graph[from_v] = [to_v]
    else:
        graph[from_v].append(to_v)


def _build_graph(formula):
    '''Builds the implication graph from the formula'''
    # Pre-allocate graph with all possible vertices
    vertices = set()
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        vertices.add((a_lit, a_neg))
        vertices.add((b_lit, b_neg))
        vertices.add((a_lit, not a_neg))
        vertices.add((b_lit, not b_neg))
    
    graph = {v: [] for v in vertices}
    
    # Add edges directly without function call overhead
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        graph[(a_lit, a_neg)].append((b_lit, not b_neg))
        graph[(b_lit, b_neg)].append((a_lit, not a_neg))
    
    return graph


def _compute_scc(graph):
    '''Computes the strongly connected components of a graph'''
    order = []
    visited = {v: False for v in graph}
    
    # Build transposed graph efficiently
    transposed = {v: [] for v in graph}
    for v, neighbors in graph.items():
        for u in neighbors:
            transposed[u].append(v)
    
    # First pass: topological ordering
    for v in graph:
        if not visited[v]:
            _dfs_transposed(v, transposed, order, visited)
    
    # Second pass: assign SCCs
    visited = {v: False for v in graph}
    vertex_scc = {}
    comp_id = 0
    
    for v in reversed(order):
        if not visited[v]:
            _dfs(v, comp_id, vertex_scc, graph, visited)
            comp_id += 1
    
    return vertex_scc


def _extract_assignment(graph, vertex_scc):
    '''Extracts variable assignment from SCC results'''
    # Early conflict detection
    seen_vars = set()
    for var, _ in graph:
        if var in seen_vars:
            continue
        seen_vars.add(var)
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None
    
    # Process components in topological order
    comp_repr = {}
    for vertex, comp in vertex_scc.items():
        if comp not in comp_repr:
            comp_repr[comp] = vertex
    
    comp_value = {}
    # Process components in reverse topological order (already sorted by comp_id)
    for comp in range(len(comp_repr)):
        if comp not in comp_value:
            comp_value[comp] = False
            lit, neg = comp_repr[comp]
            comp_value[vertex_scc[(lit, not neg)]] = True
    
    # Build result efficiently
    result = {}
    seen_vars.clear()
    for var, _ in graph:
        if var not in seen_vars:
            seen_vars.add(var)
            result[var] = comp_value[vertex_scc[(var, False)]]
    
    return result


def solve_sat(formula):
    '''Solves 2-SAT problem using implication graph and SCC'''
    graph = _build_graph(formula)
    vertex_scc = _compute_scc(graph)
    return _extract_assignment(graph, vertex_scc)


if __name__ == '__main__':
    result = solve_sat(formula)
    
    for variable, assign in result.items():
        print(f"{variable}:{assign}")