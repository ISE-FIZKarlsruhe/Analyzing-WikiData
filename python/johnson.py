# Luke Miles, September 2017
# A modification of networkx's implementation of Johnson's cycle finding algorithm
# Original implementation: https://gist.github.com/qpwo/44b48595c2946bb8f823e2d72f687cd8
# Original paper: Donald B Johnson. "Finding all the elementary circuits of a directed graph." SIAM Journal on Computing. 1975.
import csv
from sys import stdout
from collections import defaultdict
import argparse


####File parameter
#----------------------------------------------------------------
#inputfile = "../wikidata/wikidata_objects.csv"
#inputfile = "../../WikiData/py/smallgraph4.csv"
inputfile = "../../WikiData/results/nozerodeg.csv"
inputfile = "../../WikiData/results/nozerodegpandas.csv"
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile", default=inputfile, action="store")
parser.add_argument("--verbose", help="increase output verbosity",
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

    # read csv file and build the dictionary
def buildDirected(inputfile):
    dictionary = defaultdict(list);
    i = 0;
    with open(inputfile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        print("Building up the main dictionary", end=" ")
        for key, value in reader:
            dictionary[int(key)].append(int(value))
            i = i + 1;
            if (i % 3100000 == 0):
                print(".", end=" ")
        print("\nDictionary built successfully!\n")
        return dictionary

##example:
dictionary = buildDirected(inputfile)
#for key,value in dictionary.items():
#    print(key,value)

#graph = {0: [7, 3, 5], 1: [2], 2: [7, 1], 3: [0, 5], 4: [6, 8], 5: [0, 3, 7], 6: [4, 8], 7: [0, 2, 5, 8], 8: [4, 6, 7]}
graph = dictionary
for c in tuple(simple_cycles(graph)):
   for e in c:
       print(e, end=" ")
   print(c[0],end="")
   print()