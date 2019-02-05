from numvc_lib import numvclib
import networkx as nx
n = 30
graph = nx.generators.random_graphs.barabasi_albert_graph(n,10)

# graph = nx.Graph([(0,1), (1,2)])
api = numvclib()

# api.test()
print api.get_mis(nx.adjacency_matrix(graph), 0.1)
