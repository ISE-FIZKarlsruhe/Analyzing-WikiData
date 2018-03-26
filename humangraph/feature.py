#!/usr/bin/env python
from __future__ import division
import numpy as np
import csv
from collections import defaultdict
import snap
from sys import stdout
import argparse
import itertools as it

####File parameter
#----------------------------------------------------------------
inputfile = "../results/humangraph.csv"
#inputfile = "../py/smallgraph5.csv"
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile. Must be a two column .csv", default=inputfile, action="store")
parser.add_argument("--verbose", "-v", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
inputfile = args.file
if args.verbose:
    print("Inputfile:",inputfile)

def main():
    for topic, persons in G1.items():
        for x,y in it.combinations(persons, 2):
            print "%d %d"%(x,y)
    print "Finished successfully"


def intuitive():
    humans = getNeighbors(5)
    length = len(humans)
    i = 0;
    for person in humans:
        #print person, i+1
        i += 1
        j = i
        while j < length:
            nextperson = humans[j]
            Nbrs = snap.TIntV()
            comnNbr = snap.GetCmnNbrs(G1,person,nextperson, Nbrs)
            if comnNbr > 2:
                print person,nextperson,comnNbr-1,"Shared Neighbors:",
                for NId in Nbrs:
                    if NId != 5 and NId != 6581097:
                        print "%d" % NId,
                print ""
            j += 1
    print "Finished successfully"

def getNeighbors(nodeId):
    if args.verbose:
        print "Get list of humans..."
    neighborlist = []
    node = G1.GetNI(nodeId)
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

G1 =  buildUndirected()
G1 =  buildReverse()
main()