# -*- coding: utf-8 -*-
"""
A NetworkX based implementation of Yen's algorithm for computing K-shortest paths.   
Yen's algorithm computes single-source K-shortest loopless paths for a 
graph with non-negative edge cost. For more details, see: 
http://en.m.wikipedia.org/wiki/Yen%27s_algorithm
"""
__author__ = 'Guilherme Maia <guilhermemm@gmail.com>'

__all__ = ['k_shortest_paths']

from heapq import heappush, heappop
from itertools import count

import networkx as nx
import copy as cp

def k_shortest_paths(G, source, target, k = 1, weight = 'weight'):
    
    A = [nx.dijkstra_path(G, source, target, weight = 'weight')]
    A_len = [sum([G[A[0][l]][A[0][l + 1]]['weight'] for l in range(len(A[0]) - 1)])]
    B = []

    for i in range(1, k):
        for j in range(0, len(A[-1]) - 1):
            Gcopy = cp.deepcopy(G)
            spurnode = A[-1][j]
            rootpath = A[-1][:j + 1]
            for path in A:
                if rootpath == path[0:j + 1]: #and len(path) > j?
                    if Gcopy.has_edge(path[j], path[j + 1]):
                        Gcopy.remove_edge(path[j], path[j + 1])
                    if Gcopy.has_edge(path[j + 1], path[j]):
                        Gcopy.remove_edge(path[j + 1], path[j])
            for n in rootpath:
                if n != spurnode:
                    Gcopy.remove_node(n)
            try:
                spurpath = nx.dijkstra_path(Gcopy, spurnode, target, weight = 'weight')
                totalpath = rootpath + spurpath[1:]
                if totalpath not in B:
                    B += [totalpath]
            except nx.NetworkXNoPath:
                continue
        if len(B) == 0:
            break
        lenB = [sum([G[path[l]][path[l + 1]]['weight'] for l in range(len(path) - 1)]) for path in B]
        B = [p for _,p in sorted(zip(lenB, B))]
        A.append(B[0])
        A_len.append(sorted(lenB)[0])
        B.remove(B[0])
        
    return A, A_len