import ctypes
import networkx as nx
import numpy as np
import os
import sys
import scipy.sparse as sp

class numvclib(object):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.lib = ctypes.CDLL("{}/libnumvc.so".format(dir_path))
        self.lib.Numvc.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_float]

    def __CtypeNetworkX(self, g):
        edges = g.edges()
        e_list_from = (ctypes.c_int * len(edges))()
        e_list_to = (ctypes.c_int * len(edges))()

        if len(edges):
            a, b = zip(*edges)
            e_list_from[:] = a
            e_list_to[:] = b

        return (len(g.nodes()), len(edges), ctypes.cast(e_list_from, ctypes.c_void_p), ctypes.cast(e_list_to, ctypes.c_void_p))

    def __CtypeAdj(self, adj):
        adj = adj.tocoo()
        num_edge = adj.nnz
        num_node = adj.shape[0]
        e_list_from = (ctypes.c_int * num_edge)()
        e_list_to = (ctypes.c_int * num_edge)()
        edges = zip(adj.row, adj.col)
        if num_edge:
            a, b = zip(*edges)
            e_list_from[:] = [x+1 for x in a]
            e_list_to[:] = [x+1 for x in b]
        return (num_node, num_edge, ctypes.cast(e_list_from, ctypes.c_void_p), ctypes.cast(e_list_to, ctypes.c_void_p))


    def get_mis(self, adj, cutoff_time):
        n_nodes, n_edges, e_froms, e_tos = self.__CtypeAdj(sp.triu(adj))
        mis = (ctypes.c_int * (n_nodes+1))()
        mis_size = self.lib.Numvc(n_nodes, n_edges, e_froms, e_tos, mis, cutoff_time)
        mis = np.asarray(mis[1:])
        assert np.sum(mis) == mis_size
        return mis, mis_size

    def test(self):
        i = self.lib.test()
        print i
