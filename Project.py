'''
Algorithmic Thinking (Part 1)
Connected Components and Graph Resilience
'''

import random
from collections import deque
import examples

def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph 
    and the node start_node 
    and returns the set consisting of 
    all nodes that are visited by 
    a breadth-first search that starts at start_node.
    """
    visited_queue = deque()
    visited = set([start_node])
    visited_queue.append(start_node)
    while len(visited_queue) >= 1:
        other_node = visited_queue.popleft()
        for neighbor in ugraph[other_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                visited_queue.append(neighbor)
   
    return visited
    
def cc_visited(ugraph):
    """
    returns a list of sets, where each set consists of
    all the nodes (and nothing else) 
    in a connected component.
    """
    remaining_nodes = set(ugraph.keys())
    connected = []
    while len(remaining_nodes) >= 1:
        node = remaining_nodes.pop()
        visited = bfs_visited(ugraph, node)
        connected.append(visited)
        remaining_nodes.difference_update(visited)
        
    return connected
    
def largest_cc_size(ugraph):
    """
    returns the size (an integer) of 
    the largest connected component in ugraph.
    """
    largest_component = max(cc_visited(ugraph), key = len) if ugraph else []
    return len(largest_component)   
    
def compute_resilience(ugraph, attack_order):
    '''
    return a list whose k + 1 th entry is the size of 
    the largest connected component in the graph 
    after the removal of the first k nodes in attack_order.
    '''
    resilience = [largest_cc_size(ugraph)]
    for item in attack_order:
        ugraph.pop(item)
        for idx in ugraph:
            ugraph[idx].discard(item)            
        resilience.append(largest_cc_size(ugraph))
    
    return resilience
    
#print compute_resilience(examples.GRAPH0, [1, 2])    
