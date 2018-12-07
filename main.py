import networkx as nx
from mvc_greedy import mvc, mvc_random
from ls_numvc_python import numvc
from mvc_approx_greedy import mvc_approx_greedy, mvc_approx_greedy_K, mvc_approx_greedy_connectivity
from numvc import get_numvc



if __name__ == "__main__":
    graph = nx.barabasi_albert_graph(n=200,m=2)
    print "graph nodes:{} edges:{}".format(graph.number_of_nodes(), graph.number_of_edges())

    vc = get_numvc(graph, 1)
    print "C++ original numvc output - vc size: {}".format(len(vc))

    vc = numvc(graph, 10)
    print "pythonic numvc output - vc size: {}".format(len(vc))

    vc = mvc(graph)
    print "mvc_greedy - vc size: {}".format(len(vc))

    vc = mvc_random(graph)
    print "greedy mvc_random output - vc size: {}".format(len(vc))

    vc = mvc_approx_greedy(graph)
    print "mvc_approx_greedy output - vc size: {}".format(len(vc))


    vc = mvc_approx_greedy_K(graph, K=10)
    print "mvc_approx_greedy_K output - vc size: {}".format(len(vc))

    vc = mvc_approx_greedy_connectivity(graph)
    print "mvc_approx_greedy_connectivity output - vc size: {}".format(len(vc))
