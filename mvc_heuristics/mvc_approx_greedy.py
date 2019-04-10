# A greedy approach for MVC that greedily picks the uncovered edge with maximum sum of degrees of its endpoints
# This approach is used in https://arxiv.org/abs/1704.01665 as a benchmark

import networkx as nx
import os
import numpy as np
import time
import random

def mvc_approx_greedy(graph):
    edges = sorted(graph.edges, key = lambda (x,y): - graph.degree(x) - graph.degree(y))
    cost = {u:1 for u in range(graph.number_of_nodes())}
    for u,v in edges:
            min_cost = min(cost[u], cost[v])
            cost[u] -= min_cost
            cost[v] -= min_cost
    return {u for u,v in cost.iteritems() if v ==0}


# with random tie breaks
def compare(x,y):
    if x < y:
        return -1
    elif x > y:
        return 1
    else:
        return random.randint(0,1)*2 - 1

def mvc_approx_greedy_K(graph, K=1, cutoff_time = 1800):
    best_solution = np.finfo(np.float).max
    cost = {u:1 for u in range(graph.number_of_nodes())}
    for i in range(K):
        edges = sorted(graph.edges, key = lambda (x,y): - graph.degree(x) - graph.degree(y), cmp = compare)
        for u,v in edges:
            min_cost = min(cost[u], cost[v])
            cost[u] -= min_cost
            cost[v] -= min_cost

        vc = {u for u,v in cost.iteritems() if v ==0}
        if len(vc) < best_solution:
            best_solution = len(vc)
            best_vc = vc
    return best_vc

# with updating connectivity; extremely slow version
def mvc_approx_greedy_connectivity(graph):
    # We are going to modify the graph
    graph = graph.copy()
    vc = set()
    while graph.number_of_edges() > 0:
        sorted_edges = sorted(graph.edges, key = lambda (x,y): - graph.degree(x) - graph.degree(y))
        u,v = sorted_edges[0]
        vc.add(u)
        vc.add(v)
        graph.remove_node(u)
        graph.remove_node(v)
    return vc



if __name__ == "__main__":
    graph = nx.barabasi_albert_graph(n=200,m=2)
    print "graph nodes:{} edges:{}".format(graph.number_of_nodes(), graph.number_of_edges())

    vc = mvc_approx_greedy(graph)
    print "single iteration ApproxGreedy vc size: {}".format(len(vc))

    vc = mvc_approx_greedy_K(graph, K = 10)
    print "random tie breaks ApproxGreedy, vc size: {}".format(len(vc))

    vc = mvc_approx_greedy_connectivity(graph)
    print "Update connectivity ApproxGreedy, vc size: {}".format(len(vc))
