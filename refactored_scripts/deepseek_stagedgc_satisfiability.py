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


def dfs_iterative(start, graph, visited, process_vertex=None):
    """Generic iterative DFS with optional vertex processing."""
    stack = [start]
    while stack:
        v = stack.pop()
        if visited[v]:
            continue
        visited[v] = True
        
        if process_vertex:
            process_vertex(v)
            
        for u in graph[v]:
            if not visited[u]:
                stack.append(u)


def dfs_transposed(v, graph_transposed, order, visited):
    """DFS on transposed graph to compute finishing times."""
    def process_vertex(vertex):
        order.append(vertex)
    
    dfs_iterative(v, graph_transposed, visited, process_vertex)


def find_strongly_connected_components(graph):
    """Computes strongly connected components using Kosaraju's algorithm."""
    # Build transposed graph
    transposed = {vertex: [] for vertex in graph}
    for v, neighbors in graph.items():
        for u in neighbors:
            transposed[u].append(v)
    
    # First pass: compute finishing times
    visited = {vertex: False for vertex in graph}
    order = []
    for v in graph:
        if not visited[v]:
            dfs_transposed(v, transposed, order, visited)
    
    # Second pass: find SCCs
    visited = {vertex: False for vertex in graph}
    vertex_scc = {}
    current_component = 0
    
    for v in reversed(order):
        if not visited[v]:
            def assign_component(vertex):
                vertex_scc[vertex] = current_component
            dfs_iterative(v, graph, visited, assign_component)
            current_component += 1
    
    return vertex_scc


def build_implication_graph(formula):
    """Builds the implication graph from the 2-CNF formula."""
    # Collect all variables
    variables = set()
    for (a_lit, _), (b_lit, _) in formula:
        variables.add(a_lit)
        variables.add(b_lit)
    
    # Initialize graph with all literals
    graph = {}
    for var in variables:
        graph[(var, False)] = []
        graph[(var, True)] = []
    
    # Add implication edges
    for (a_lit, a_neg), (b_lit, b_neg) in formula:
        # (a ∨ b) ≡ (¬a → b) ∧ (¬b → a)
        graph[(a_lit, a_neg)].append((b_lit, not b_neg))
        graph[(b_lit, b_neg)].append((a_lit, not a_neg))
    
    return graph


def extract_variables_from_graph(graph):
    """Extracts unique variable names from graph vertices."""
    return {v[0] for v in graph}


def solve_2sat(formula):
    """Solves 2-SAT problem using implication graph and SCC decomposition."""
    if not formula:
        return {}
    
    graph = build_implication_graph(formula)
    vertex_scc = find_strongly_connected_components(graph)
    variables = extract_variables_from_graph(graph)
    
    # Check for contradictions (x and ¬x in same SCC)
    for var in variables:
        if vertex_scc[(var, False)] == vertex_scc[(var, True)]:
            return None
    
    # Assign values based on SCC topological order
    component_value = {}
    for var in variables:
        false_component = vertex_scc[(var, False)]
        true_component = vertex_scc[(var, True)]
        
        # Assign False to the component that appears earlier in topological order
        if false_component not in component_value:
            component_value[false_component] = False
            component_value[true_component] = True
    
    # Build final assignment
    assignment = {}
    for var in variables:
        assignment[var] = component_value[vertex_scc[(var, False)]]
    
    return assignment


if __name__ == '__main__':
    result = solve_2sat(formula)
    
    for variable, assign in result.items():
        print(f"{variable}:{assign}")