#!/usr/bin/env python

import csv
from collections import defaultdict
import sys
import community
import networkx as nx
import matplotlib.pyplot as plt
import argparse

####File parameter
#----------------------------------------------------------------
inputfile = "../py/smallgraph4.csv"
inputfile = "../py/wikidata_objects.csv"
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile. Must be a two column .csv", default=inputfile, action="store")
args = parser.parse_args()
inputfile = args.file


def main():
    print("Searching partitions...")
    partition = community.best_partition(G)
    inv_p = invertdict(partition)
    for p in inv_p.items():
        print('Partition %d: Size: %d Items:' % (p[0],len(p[1])),p[1])

    #dendo = community.generate_dendrogram(G)
    #for level in range(len(dendo) - 1):
    #    print("partition at level", level, "is", community.partition_at_level(dendo, level))
        # drawing(community.partition_at_level(dendo, level))



def buildGraph():
    print("Building graph from %s..." % (inputfile))
    fh = open(inputfile, 'rb')
    G = nx.read_edgelist(fh, delimiter=";")
    print("Done.")
    return G
    # for e in list(G.edges): print(e)
    # nx.draw(G)
    # plt.show()

def invertdict(dict):
    inv_dict = {}
    print("Building inverted dict...")
    for k, v in dict.items():
        inv_dict.setdefault(v, []).append(k)
    print("Done.")
    return inv_dict

# def drawing(partition):
#     size = float(len(set(partition.values())))
#     pos = nx.spring_layout(G)
#     count = 0.
#     for com in set(partition.values()) :
#         count = count + 1.
#         list_nodes = [nodes for nodes in partition.keys()
#                                     if partition[nodes] == com]
#         nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
#                                     node_color = str(count / size))
#     nx.draw_networkx_edges(G, pos, alpha=0.5)
#     plt.show()

G = buildGraph()
main()
