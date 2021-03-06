'''
Algorithmic Thinking (Part 1)
Analysis of a Computer Network
'''

import random
import time
import math
import matplotlib.pyplot as plt
import timeit
import project


def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    #count = 0
    # copy the graph
    #s = time.time()
    #s = timeit.default_timer()
    new_graph = copy_graph(ugraph)
    #count += 1
    order = []    
    while len(new_graph) > 0:
        #count += 1
        max_degree = -1
        for node in new_graph:
            #count += 1
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            #count += 1
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    #print count, 'slow count'
    #e = timeit.default_timer()    
    return order#(e-s)

def fast_targeted_order(ugraph):
    #s = time.time()
    #s = timeit.default_timer()
    #count = 0
    new_graph = copy_graph(ugraph)
    #count += 1
    degree_sets = []
    #count += 1
    for m in range(len(new_graph)):
        degree_sets.append(set())
        #count += 1
    for i in new_graph:
        d = len(new_graph[i])
        degree_sets[d].add(i)
        #count += 1
    L = []
    #count += 1
    for k in range(len(new_graph.keys()) - 1, -1, -1):
        #count += 1
        while degree_sets[k]:
            #count += 1
            u = degree_sets[k].pop()
            nei = new_graph[u]
            for v in nei:
                #count += 1
                d = len(new_graph[v])
                degree_sets[d].remove(v)
                degree_sets[d-1].add(v)    
            L.append(u)    
            delete_node(new_graph, u)
    #print count, 'count fast'
    #e = timeit.default_timer()        
    return L #(e-s)

  
##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def ER(n, p):
    """
    Generate a random undirected graph with probability p
    """
    ans = {}
    for node in range(n):
        if node not in set(ans.keys()):
            ans[node] = set([])
        for edge in range(n):
            if edge != node:
                a = random.random()
                if a < p:
                    if edge not in set(ans.keys()):
                        ans[edge] = set([node])
                    else:
                        ans[edge].add(node)
                    ans[node].add(edge)                    
    return ans

def num_edges(graph):
    """
    returns number of edges in a graph
    """
    ans = []
    for val in graph.values():
        ans += list(val)
    return len(ans) / 2
    
"""
Provided code for application portion of module 2

Helper class for implementing efficient version
of UPA algorithm
"""

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    
def make_complete_graph(num_nodes):
    """
    This function generate the complete directed graph with
    the given number of vertices.
    """
    
    comp_graph = {}
    all_vertex = set(range(num_nodes))
    
    for dumy_vertex in all_vertex:
        copy_vertex = all_vertex.copy()
        copy_vertex.remove(dumy_vertex)
        comp_graph[dumy_vertex] = set(copy_vertex)
        
    return comp_graph

def UPA(n, m):
    """
    makes random graphs
    """
    graph = make_complete_graph(m)
    obj = UPATrial(m)
    for i in range(m, n):
        x = obj.run_trial(m)
        graph[i] = x
        for node in x:
            graph[node].add(i)
        
    return graph

def random_order(graph):
    """
    returns the nodes in the graph shuffeled
    """
    ans = graph.keys()
    random.shuffle(ans)
    return ans

def run(n):
    """
    a function to run the algorthims on different inputs
    """
    d1 = []
    d2 = []
    d3 = []
    for i in n:
        x = UPA(i, 5)
        d3.append(i)
        s1 = timeit.default_timer()
        targeted_order(x)
        e1 = timeit.default_timer()
        s2 = timeit.default_timer()
        fast_targeted_order(x)
        e2 = timeit.default_timer()
        d1.append((e1-s1))
        d2.append((e2-s2))
    #print d1    
    plt.plot(d3, d1, label = 'regular function')
    plt.plot(d3, d2, '-r', label = 'fast function')
    plt.legend(loc='upper right')
    plt.title('running times of targeted_order vs fast_targeted_order using desktop python')
    plt.xlabel('size of the UPA graph with m = 5')
    plt.ylabel('running time in seconds')
    plt.show()


#run(range(10, 1000, 10))    
# IMPORTANT p = 0.00397
# IMPORTANT m = 3
graph1 = load_graph(NETWORK_URL)
graph2 = ER(1239, 0.002)
graph3 = UPA(1239, 3)

data1 = project.compute_resilience(graph1, fast_targeted_order(graph1))
data2 = project.compute_resilience(graph2, fast_targeted_order(graph2))
data3 = project.compute_resilience(graph3, fast_targeted_order(graph3))
datax = range(1240)

plt.plot(datax, data1, '-b', label = 'computer_network')
plt.plot(datax, data2, '-y', label = 'ER graph with p = 0.00397')
plt.plot(datax, data3, '-r', label = 'UPA graph with m = 3')

plt.legend(loc='upper right')
plt.xlabel("Number of removed nodes")
plt.ylabel("Size of the Largest Component")
plt.title("The Resilience of Different Types of Networks after a targeted attack")

plt.show()
  



