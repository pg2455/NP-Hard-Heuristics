#Greedy version of mvc
#As discussed in Christos H. Papadimitriou and Kenneth Steiglitz. Combinatorial Optimization: Algorithms and Complexity
#code in mvc() is from networkx library

import networkx as nx
import os
import numpy as np
import time
import random

def mvc(graph):
    cost = {u:1 for u in range(graph.number_of_nodes())}
    for u,v in graph.edges:
        min_cost = min(cost[u], cost[v])
        cost[u] -= min_cost
        cost[v] -= min_cost
    return {u for u,v in cost.iteritems() if v ==0}


def mvc_random(graph, K = 100):
    best_solution  = np.finfo(np.float).max
    best_vc = {}
    edges = list(graph.edges)
    for _ in range(K):
        cost = {u:1 for u in range(graph.number_of_nodes())}
        np.random.shuffle(edges)
        for u,v in edges:
            min_cost = min(cost[u], cost[v])
            cost[u] -= min_cost
            cost[v] -= min_cost
    vc = {u for u,v in cost.iteritems() if v ==0}
    if len(vc) < best_solution:
        best_solution = len(vc)
        best_vc = vc

    return best_vc

if __name__ == "__main__":
    graph = nx.barabasi_albert_graph(n=200,m=2)
    print "graph nodes:{} edges:{}".format(graph.number_of_nodes(), graph.number_of_edges())

    vc = mvc(graph)
    print "single iteration vc size: {}".format(len(vc))

    vc = mvc_random(graph)
    print "random sorted edges, vc size: {}".format(len(vc))
