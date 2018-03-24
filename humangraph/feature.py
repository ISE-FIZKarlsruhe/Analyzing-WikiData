#!/usr/bin/env python
from __future__ import division
import numpy as np
import csv
from collections import defaultdict
import snap
from sys import stdout
import argparse

####File parameter
#----------------------------------------------------------------
inputfile = "../results/humangraph"
#inputfile = "../py/smallgraph4"
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile. Must be a two column .csv", default=inputfile, action="store")
parser.add_argument("--verbose", "-v", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
inputfile = args.file
if args.verbose:
    print("Inputfile:",inputfile)

def main():
    print ""
    humans = getNeighbors(5)
    length = len(humans)
    i = 0;
    for person in humans:
        #print person, i+1
        i += 1
        j = i
        while j < length:
            nextperson = humans[j]
            comnNbr = snap.GetCmnNbrs(G1,person,nextperson)
            print person,nextperson,comnNbr-1
            j += 1

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

G1 =  buildUndirected()
main()