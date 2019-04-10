# This is a pythonic version of Local Search on MVC
# as described in https://arxiv.org/abs/1402.0584
# C++ version provided by the authors here http://lcs.ios.ac.cn/~caisw/MVC.html
# The python interface to the C++ version is implemented in numvc.py

import time, random
import networkx as nx
import numpy as np
from mvc_greedy import mvc

def numvc(graph, cutoff_time, cutoff_iter = 1000):
    GAMMA = 0.5 * graph.number_of_nodes()
    RHO = 0.3

    edge_weights = {u:1 for u in graph.edges}
    dscores = {}
    age = {u:0 for u in graph.nodes}
    confChange = {u:1 for u in graph.nodes}

    def get_cost(vc):
        uncovered_edges = get_uncovered_edges(vc)
        if len(uncovered_edges) > 0:
            return sum([edge_weights[u] for u in uncovered_edges])
        return 0

    def is_valid(vc):
        uncovered_edges = get_uncovered_edges(vc)
        if uncovered_edges:
            return False
        return True

    def update_dscores():
        x = get_cost(C)
        for v in graph.nodes:
            if v in C:
                z = C.copy()
                z.remove(v)
                y = get_cost(z)
                assert x <= y
            else:
                z = C.copy()
                z.add(v)
                y = get_cost(z)

            dscores[v] = x - y

    def get_uncovered_edges(C):
        uncovered_edges = set(graph.edges - graph.edges(C))
        Z = uncovered_edges.copy()
        for z in Z:
            if z[0] in C or z[1] in C:
                uncovered_edges.remove(z)
        return uncovered_edges

    C = mvc(graph)
    update_dscores()
    C_star = C.copy()

    start = time.time()
    iter = 0
    while time.time() - start < cutoff_time and iter < cutoff_iter:
        iter += 1

        #if iter%20 == 0: print "iter:{}, vc:{}".format(iter, len(c_star))
        if is_valid(C):
            C_star = C.copy()
            update_dscores()
            C.remove(max(C, key = lambda x:(dscores[x], iter-age[x])))
            continue

        update_dscores()
        u = max(C, key = lambda x:(dscores[x], iter-age[x]))
        C.remove(u)
        age[u] = iter
        confChange[u] = 0
        for z in graph.neighbors(u):
            confChange[z] = 1

        update_dscores()
        edge = random.choice(list(get_uncovered_edges(C)))
        v = {z for z in edge if confChange[z] == 1}
        v = max(v, key = lambda x: (dscores[x], iter - age[x]))
        C.add(v)
        age[v] = iter
        for z in graph.neighbors(v):
            confChange[z] = 1

        for z in get_uncovered_edges(C):
            edge_weights[z] += 1

        if np.mean(edge_weights.values()) >= GAMMA:
            #pdb.set_trace()
            edge_weights = {u: np.floor(RHO * v) for u,v in edge_weights.iteritems()}

    return C_star


if __name__ == "__main__":
    graph = nx.barabasi_albert_graph(n=200,m=2)
    print "graph nodes:{} edges:{}".format(graph.number_of_nodes(), graph.number_of_edges())

    vc = numvc(graph, 5)
    print "single iteration ApproxGreedy vc size: {}".format(len(vc))
