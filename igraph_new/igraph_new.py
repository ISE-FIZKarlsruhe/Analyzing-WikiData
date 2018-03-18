#!/usr/bin/env python

import igraph as ig
import csv
from collections import defaultdict
import sys
inputfile = "../py/wikidata_objects.txt"
inputfile = "../py/wikidata_objects.csv"
#inputfile = "../py/smallgraph4.txt"
#inputfile = "smallgraph4.ncol"

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
sys.stdout = Unbuffered(sys.stdout)

def main():
    #getAllShortestPaths("3")
    levels = g.community_multilevel(weights=None, return_levels=True)
    for l in levels:
        print(l)
    #getCloseness()
    #getAllShortestPaths(1)

def getCloseness():
    record = []
    for name, closeness in zip(g.vs["name"],g.closeness(mode = "OUT")):
        record.append((name, closeness))
    for vc in record:
        print(vc)

def getAllShortestPaths(start):
    print("Getting all shoretst paths...")
    asp = g.get_all_shortest_paths(start)
    asp2 = []
    for p in asp:
        q = []
        for n in p:
            q.append(int(g.vs[n]["name"]))
        asp2.append(q)
    for e in sorted(asp2,key=lambda x:x[len(x)-1]):
        print(e)

def buildList(inputfile):
    mainlist = []
    i = 0;
    with open(inputfile, newline ='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        print("Building up the main list", end=" ")
        for key, value in reader:
            mainlist.append([int(key),int(value)])
            i = i+1;
            if (i % 3000000 == 0):
                print(".", end=" ")
        print("\nList built successfully!\n")
        return mainlist

mainlist = buildList(inputfile)
print("Building Graph...")
g = ig.Graph.DictList(vertices=None, edges=({"source": subject, "target": object} for subject, object in mainlist))
#g = ig.Graph.Read_Ncol(inputfile, names=True, weights=False, directed=False)
print(" Done.")
main()