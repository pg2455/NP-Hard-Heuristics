import networkx as nx
import numpy as np

def greedy_best_independent_set(graph):
    adj_0 = nx.adj_matrix(graph).todense()
    a = -np.array([graph.nodes[u]['weight'] for u in graph.nodes])
    IS = -np.ones(adj_0.shape[0])
    while np.any(IS==-1):
        rem_vector = IS == -1
        adj = adj_0.copy()
        adj = adj[rem_vector, :]
        adj = adj[:, rem_vector]

        u = np.argmin(a[rem_vector].dot(adj!=0)/a[rem_vector])
        n_IS = -np.ones(adj.shape[0])
        n_IS[u] = 1
        neighbors = np.argwhere(adj[u,:]!=0)
        if neighbors.shape[0]:
            n_IS[neighbors] = 0
        IS[rem_vector] = n_IS

    return IS

if __name__ == "__main__":
    graph = nx.generators.random_graphs.barabasi_albert_graph(50,10)
    for u in graph:
        graph.nodes[u]['weight'] = np.random.uniform(0,1)

    print greedy_best_independent_set(graph)
