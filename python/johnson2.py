# Luke Miles, September 2017
# A modification of networkx's implementation of Johnson's cycle finding algorithm
# Original implementation: https://gist.github.com/qpwo/44b48595c2946bb8f823e2d72f687cd8
# Original paper: Donald B Johnson. "Finding all the elementary circuits of a directed graph." SIAM Journal on Computing. 1975.
import csv
import pandas as pd
from sys import stdout
from collections import defaultdict
import argparse


####File parameter
#----------------------------------------------------------------
inputfile = "../results/wikidata_supertypeGraph.csv"
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile. Must be a two column .csv", default=inputfile, action="store")
parser.add_argument("--verbose", "-v", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
inputfile = args.file
print("Inputfile:",inputfile)


def simple_cycles(G):
    # Yield every elementary cycle in python graph G exactly once
    # Expects a dictionary mapping from vertices to iterables of vertices
    def _unblock(thisnode, blocked, B):
        stack = set([thisnode])
        while stack:
            node = stack.pop()
            if node in blocked:
                blocked.remove(node)
                stack.update(B[node])
                B[node].clear()
    G = {v: set(nbrs) for (v, nbrs) in G.items()}  # make a copy of the graph
    sccs = strongly_connected_components(G)
    while sccs:
        scc = sccs.pop()
        startnode = scc.pop()
        path = [startnode]
        blocked = set()
        closed = set()
        blocked.add(startnode)
        B = defaultdict(set)
        stack = [(startnode, list(G[startnode]))]
        while stack:
            thisnode, nbrs = stack[-1]
            if nbrs:
                nextnode = nbrs.pop()
                if nextnode == startnode:
                    yield path[:]
                    closed.update(path)
                elif nextnode not in blocked:
                    path.append(nextnode)
                    stack.append((nextnode, list(G[nextnode])))
                    closed.discard(nextnode)
                    blocked.add(nextnode)
                    continue
            if not nbrs:
                if thisnode in closed:
                    _unblock(thisnode, blocked, B)
                else:
                    for nbr in G[thisnode]:
                        if thisnode not in B[nbr]:
                            B[nbr].add(thisnode)
                stack.pop()
                path.pop()
        remove_node(G, startnode)
        H = subgraph(G, set(scc))
        sccs.extend(strongly_connected_components(H))

def strongly_connected_components(graph):
    # Tarjan's algorithm for finding SCC's
    # Robert Tarjan. "Depth-first search and linear graph algorithms." SIAM journal on computing. 1972.
    # Code by Dries Verdegem, November 2012
    # Downloaded from http://www.logarithmic.net/pfh/blog/01208083168
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    result = []
    def _strong_connect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        successors = graph[node]
        for successor in successors:
            if successor not in index:
                _strong_connect(successor)
                lowlink[node] = min(lowlink[node], lowlink[successor])
            elif successor in stack:
                lowlink[node] = min(lowlink[node], index[successor])
        if lowlink[node] == index[node]:
            connected_component = []
            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            result.append(connected_component[:])
    for node in graph:
        if node not in index:
            _strong_connect(node)
    return result


def remove_node(G, target):
    # Completely remove a node from the graph
    # Expects values of G to be sets
    del G[target]
    for nbrs in G.values():
        nbrs.discard(target)


def subgraph(G, vertices):
    # Get the subgraph of G induced by set vertices
    # Expects values of G to be sets
    return {v: G[v] & vertices for v in vertices}

def buildDataframe(inputfile):
    dataframe = pd.read_csv(inputfile, sep=";", names=["0", "1"])
    return dataframe

def removeZeroDeg(dataframe):
    i = 0;
    removed = True
    while removed == True:
        i += 1
        if args.verbose:
            print(i, "iteration:")
        size_bef = dataframe.shape[0]
        dataframe = dataframe.loc[dataframe['0'].isin(dataframe['1'])]
        dataframe = dataframe.loc[dataframe['1'].isin(dataframe['0'])]
        size_aft = dataframe.shape[0]
        if args.verbose:
            print("---removing:", size_bef - size_aft)
        removed = (size_bef != size_aft)
    return dataframe

    # read csv file and build the dictionary
def buildDirected(dataframe):
    dictionary = defaultdict(list);
    for index, row in dataframe.iterrows():
        dictionary[int(row["0"])].append(int(row["1"]))
    if args.verbose:
        print("\nDictionary built successfully!\n")
    return dictionary

##example:
dataframe = buildDataframe(inputfile)
dataframe = removeZeroDeg(dataframe)
graph = buildDirected(dataframe)

for c in tuple(simple_cycles(graph)):
   for e in c:
       print(e, end=" ")
   print(c[0],end="")
   print()