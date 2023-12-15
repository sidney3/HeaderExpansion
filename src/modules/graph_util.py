from typing import Dict, Collection, DefaultDict, TypeVar, Iterable, List, Set
from collections import defaultdict
"""
GRAPH RELATED UTILITY FUNCTIONS.
"""
T = TypeVar('T')
def get_required_components(graph: Dict[T, Collection[T]], base: Collection[T]) -> Collection[T]:
    """
    Given a graph and a subset of nodes from the graph, returns all nodes reachable from these
    nodes, sorted in proper ordering

    Throws:
        Exception (Cyclic Dependencies): the graph must be a directed acyclic graph
    """
    node_order: dict[T, int] = __topo_sort(graph)
    visited: Set[T] = set()
    def dfs(curr_node: T):
        if curr_node in visited:
            return
        visited.add(curr_node)
        for next_node in graph[curr_node]:
            dfs(next_node)
    for node in base:
        dfs(node)
    return sorted(visited, key = lambda node: node_order[node])
def __topo_sort(graph: Dict[T, Collection[T]]) -> Dict[T, int]:
    """
    Given an arbitrary graph, returns a topological sorting of its
    components that is given by a dictionary from node to its order
    """
    if __check_cycles(graph):
        raise Exception("Cyclic Dependencies")
    sorted_components: List[T] = [] 
    visited: Set[T] = set()
    def topo(curr_node: T):
        if curr_node in visited:
            return
        for next_node in graph[curr_node]:
            topo(next_node)
        sorted_components.append(curr_node)
    for node in graph:
        topo(node)
    return {comp: order for order, comp in enumerate(reversed(sorted_components))}
def __check_cycles(graph: Dict[T, Collection[T]]) -> bool:
    """
    Given an arbitrary directed graph, checks for cycles
    """
    UNVISITED, VISITING, VISITED = 0,1,2
    graph_state: DefaultDict[T, int] = defaultdict(lambda: UNVISITED)
    def dfs(curr_node: T):
        if(graph_state[curr_node] == VISITED):
            return False
        if(graph_state[curr_node] == VISITING):
            return True
        graph_state[curr_node] = VISITING
        found_cycle = False
        for next_node in graph[curr_node]:
            found_cycle = found_cycle or dfs(next_node)
        graph_state[curr_node] = VISITED
        return found_cycle 
    is_cycle = False
    for node in graph:
        is_cycle = is_cycle or dfs(node)
    return is_cycle

