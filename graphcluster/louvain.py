#!/usr/bin/env python
import community
import networkx as nx
# import matplotlib.pyplot as plt
import argparse

### INFO ###
# running on python 3.5
# inputfile is .csv

####File parameter
# ----------------------------------------------------------------
inputfile = "../py/smallgraph7_relational.csv"
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile. Must be a two column .csv",
                    default=inputfile, action="store")
parser.add_argument("--levels", "-l", help="prints results for all levels", action="store_true")
parser.add_argument("--members", "-m", help="shows the members within each cluster instead of the cluster's size",
                    action="store_true")
args = parser.parse_args()
inputfile = args.file


def main():
    print("Searching partitions...")
    partition = community.best_partition(G)
    print("Done.")
    inv_p = invertdict(partition)
    for p in inv_p.items():
        if args.members:
            print('Partition %d: Size: \'%d\' Members: %s' % (p[0], len(p[1]), p[1]))
        else:
            print('Partition %d: Size: %d' % (p[0], len(p[1])))

    if args.levels:
        print("\nPrinting all Levels...")
        dendo = community.generate_dendrogram(G)
        for level in range(len(dendo)):
            print("partition at level", level, "is", community.partition_at_level(dendo, level))
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


def buildWeightedGraph():
    print("Building weighted graph from %s..." % (inputfile))
    fh = open(inputfile, 'rb')
    G = nx.read_weighted_edgelist(fh, delimiter=";")
    print("Done.")
    return G


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
