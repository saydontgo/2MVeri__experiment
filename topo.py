#!/usr/bin/env python3

import networkx as nx
import json
import sys

from pip import main

prime_table = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

class Topology:
    def __init__(self, topo_json):
        self.graph = nx.Graph()
        
        self.nodes = []
        self.primes = {}
        # parse topology 
        with open(topo_json, 'r') as json_file:
            topo = json.load(json_file)
            i = 0
            for node in topo['nodes']:
                self.nodes.append(node['id'])
                
                if 'isHost' in node and node['isHost']:
                    self.primes[node['id']] = 1
                else:
                    self.primes[node['id']] = prime_table[i]
                    i = i + 1
                # self.primes.append(node['prime'])
                
            self.graph.add_nodes_from(self.nodes)
            #parse the links
            for link in topo['links']:
                self.graph.add_edge(link['source'], link['target'])
        
    def get_graph(self):
        return self.graph

    def get_nodes(self):
        return self.nodes
    
    def get_primes(self):
        return self.primes
    
    def get_prime(self, node):
        return self.primes[node]
    
    def get_neighbors(self, node):
        return self.graph.neighbors(node)

    def get_paths(self, s, t, len, number):
        paths = []
        #diffTime = 0
        #t0 = time.time()
        paths = nx.all_simple_paths(self.graph, source=s, target=t, cutoff=len)
        #t1 = time.time()
        #diffTime = t1 - t0
        #print("Graph traversal time %s: %s" % (number, diffTime))
        return list(paths)

    def get_paths_no_cutoff(self, s, t, number):
        paths = []
        #diffTime = 0
        #t0 = time.time()
        paths = nx.all_simple_paths(self.graph, source=s, target=t)
        #t1 = time.time()
        #diffTime = t1 - t0
        #print("Graph traversal time without cutoff %s: %s" % (number, diffTime))
        return list(paths)

if __name__ == '__main__':
    topo = Topology('./topology.json')
    print(topo.primes)
    # print(topo.get_paths_no_cutoff('h1', 's4', 1))
    print([n for n in topo.get_neighbors('h15')])
    
    # prime_prod = 2423602
    # tmp_prod = prime_prod
    # pre_switch = None
    # end_switch = 'h15'
    # path = [end_switch]
    # while tmp_prod > 1:
    #     flag = False
    #     for node in topo.get_neighbors(end_switch):
    #         if pre_switch == None or node != pre_switch:
    #             prime = topo.get_prime(node)
    #             if prime == 1:
    #                 continue
    #             if tmp_prod % prime == 0:
    #                 pre_switch = end_switch
    #                 end_switch = node
    #                 tmp_prod = tmp_prod / prime
    #                 flag = True
    #                 break
                
    #     if flag :
    #         path.append(end_switch)
    #         # print("tmp_prod: %s, forward path: %s"% (tmp_prod, path))
    #     else:
    #         print("prime product: %s not recover actual forward path" % (prime_prod))
    #         sys.exit()
    #     print("forward path: %s"% (path))
              
    # print("forward path: %s"% (path))