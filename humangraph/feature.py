#!/usr/bin/env python
from __future__ import division
import numpy as np
import csv
from collections import defaultdict
import snap
from sys import stdout
import argparse
import itertools as it
import time

####File parameter
#----------------------------------------------------------------
inputfile = "../results/humangraph.csv"
inputfile = "../py/smallgraph5.csv"
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile. Must be a two column .csv", default=inputfile, action="store")
parser.add_argument("--verbose", "-v", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
inputfile = args.file
if args.verbose:
    print("Inputfile:",inputfile)

def main():
    G1 = buildReverse()
    third(G1)

    #for topic, persons in G1.items():
    #    print "%d %d"%(topic, len(persons))
    #print "Finished successfully"

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

def second(graph):
    excluded = [5, 6581097, 6581072]
    for topic, persons in graph.items():
        c = 0
        start_time = time.clock()
        if not topic in excluded:
            for x,y in it.combinations(persons, 2):
                #print "%d %d"%(x,y)
                c += 1
            print "T %d, count %d, time %s"%(topic, c, secondsToStr(time.clock() - start_time))

def third(graph):
    edgelist = defaultdict(int);
    excluded = [5, 6581097, 6581072]        #removing "human", "male", "female"
    threshold = 3                           #min common neighbors to be counted "connected" in the end
    topiccounter = 0
    for e in excluded:
        try:
            del graph[e]
        except:
            print("Excluded value not in graph.")   #to be able to test on smallgraph5.csv
    print "Bulildung Edge-Dictionary..."
    for topic, persons in graph.items():
        topiccounter = topiccounter+1
        print "Count: %d, Name: %d"%(topiccounter, topic)
        for x,y in it.combinations(persons, 2):
            if y != None:
                edgelist[frozenset((x,y))] +=1
    print "Done."
    print "Printing the Edgelist"
    for edge in edgelist.items():
        if edgelist[edge[0]]>=threshold:
            for p in edge[0]:
                print p,
            print edge[1]

def first(graph):
    humans = getNeighbors(graph,5)
    length = len(humans)
    i = 0;
    for person in humans:
        #print person, i+1
        i += 1
        j = i
        while j < length:
            nextperson = humans[j]
            Nbrs = snap.TIntV()
            comnNbr = snap.GetCmnNbrs(graph,person,nextperson, Nbrs)
            if comnNbr > 2:
                print person,nextperson,comnNbr-1,"Shared Neighbors:",
                for NId in Nbrs:
                    if NId != 5 and NId != 6581097:
                        print "%d" % NId,
                print ""
            j += 1

def getNeighbors(graph,nodeId):
    if args.verbose:
        print "Get list of humans..."
    neighborlist = []
    node = graph.GetNI(nodeId)
    deg = node.GetInDeg()
    for i in range(0, deg):
        neighborlist.append(node.GetNbrNId(i))
    neighbors = np.array(neighborlist)
    if args.verbose:
        print "Done."
    return neighbors

def buildUndirected():
    if args.verbose:
        print "Building undirected graph from",inputfile
    G1 = snap.LoadEdgeList(snap.PUNGraph, inputfile, 0, 1)
    if args.verbose:
        print "Done."
    return G1

def buildReverse():
    reverse = defaultdict(list);
    with open(inputfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        if args.verbose:
            print "Buildung up the reverse dictionary",
        for key, value in reader:
            reverse[int(value)].append(int(key))
        if args.verbose:
            print "\nDictionary built successfully!\n"
        return reverse
main()