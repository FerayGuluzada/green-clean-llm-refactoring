"""
Given a formula in conjunctive normal form (2-CNF), finds a way to assign
True/False values to all variables to satisfy all clauses, or reports there
is no solution.

https://en.wikipedia.org/wiki/2-satisfiability
"""

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


class GraphSolver:
    """Encapsulates graph operations for 2-SAT solving."""
    
    @staticmethod
    def dfs(v, graph, visited, order=None, component=None, vertex_comp=None):
        """Generic DFS for topological order and component assignment."""
        stack = [v]
        visited[v] = True
        
        while stack:
            current = stack[-1]
            found_unvisited = False
            
            for neighbor in graph.get(current, []):
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
                    found_unvisited = True
                    break
            
            if not found_unvisited:
                node = stack.pop()
                if order is not None:
                    order.append(node)
                if component is not None and vertex_comp is not None:
                    vertex_comp[node] = component
    
    @staticmethod
    def scc(graph):
        """Computes strongly connected components using Kosaraju's algorithm."""
        # First pass: topological order on transposed graph
        transposed = {v: [] for v in graph}
        for v, neighbors in graph.items():
            for u in neighbors:
                transposed[u].append(v)
        
        visited = {v: False for v in graph}
        order = []
        
        for v in graph:
            if not visited[v]:
                GraphSolver.dfs(v, transposed, visited, order=order)
        
        # Second pass: assign components in reverse order
        visited = {v: False for v in graph}
        vertex_comp = {}
        component_id = 0
        
        for v in reversed(order):
            if not visited[v]:
                GraphSolver.dfs(v, graph, visited, component=component_id, vertex_comp=vertex_comp)
                component_id += 1
        
        return vertex_comp


def build_graph(formula):
    """Builds implication graph from 2-CNF formula."""
    graph = {}
    
    # Initialize all possible literals
    for (lit_a, _), (lit_b, _) in formula:
        for lit, neg in [(lit_a, False), (lit_a, True), (lit_b, False), (lit_b, True)]:
            graph.setdefault((lit, neg), [])
    
    # Add implication edges
    for (lit_a, neg_a), (lit_b, neg_b) in formula:
        graph[(lit_a, neg_a)].append((lit_b, not neg_b))
        graph[(lit_b, neg_b)].append((lit_a, not neg_a))
    
    return graph


def solve_sat(formula):
    """Solves 2-SAT problem using implication graph analysis."""
    graph = build_graph(formula)
    vertex_comp = GraphSolver.scc(graph)
    
    # Check for contradictions
    for var in {var for (var, _) in graph}:
        if vertex_comp[(var, False)] == vertex_comp[(var, True)]:
            return None
    
    # Assign values based on component order
    comp_value = {}
    for vertex, comp_id in vertex_comp.items():
        if comp_id not in comp_value:
            var, neg = vertex
            comp_value[comp_id] = False
            comp_value[vertex_comp[(var, not neg)]] = True
    
    # Extract variable assignments
    return {var: comp_value[vertex_comp[(var, False)]] for (var, _) in graph}


if __name__ == '__main__':
    result = solve_sat(formula)
    
    for variable, assign in result.items():
        print(f"{variable}:{assign}")