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
import pandas as pd
import bisect

####File parameter
#----------------------------------------------------------------
inputfile = "../results/humangraph.csv"
inputfile = "../results/humangraph10_notrivial.csv"
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
    #G1 = buildReverse()
    #secondMulti(G1)
    #third(G1)

    G1 = buildDirectedDict(inputfile)
    fourth(G1,2)

def fourth(graph, threshold):
    threshold = threshold
    edgelist = pd.read_csv(inputfile, sep=";", header=None)
    n = 0
    #print "\nEDGELIST"
    #for index, row in edgelist.iterrows():
    #    print row[0], row[1]

    print "\nPerson1 Person2 Weight"
    for person in graph.items():
        n = n+1
        print "\n------person",person[0],"-------number", n
        size = len(person[1])
        edgelist = edgelist[size:]

        #Debugging
        #print "\n-------------EDGELIST",person[0]
        #for index, row in edgelist.iterrows():
        #    print row[0], row[1]

        ###Version One [to find all 2-step persons and return them in a sorted list]
        #as list
        #nbrP = edgelist.loc[edgelist[1].isin(person[1])][0].values.tolist()
        nbrP = np.array(edgelist.loc[edgelist[1].isin(person[1])][0].values)
        print nbrP

        ###Version Two
        #nbrT = pd.DataFrame(person[1])
        #nbrP = np.sort(pd.merge(edgelist, nbrT, left_on=1, right_on=0, how='inner')["0_x"])
        #print nbrP

        #### Method One [To find occurences above threshold]
        #intutive iteration
        # d = 0
        # c = 0
        # for e in nbrP:
        #     #if e == person[0]:
        #     #    continue
        #     if e == d:
        #         c = c+1
        #     else:
        #         if c >= threshold:
        #             print person[0], d, c
        #         d = e
        #         c = 1
        # if c >= threshold:
        #     print person[0], d, c

        #### Method Two [To find occurences above threshold]
        #threshold related jumps
        #zuletzt ausgegebene Zahl
        lastprint = 0
        #wenn liste nicht leer
        if nbrP.any():
            current = nbrP[0]
        i = 0
        while i + threshold - 1 < len(nbrP):
            prev = current
            i += threshold - 1
            current = nbrP[i]
            if current == prev and current != lastprint:
                print person[0], current
                lastprint = current
            else:
                for j in xrange(i - 1, (i - threshold), -1):
                    if nbrP[j] != current:
                        i = j + 1
                        break

        #### Method Three [To find occurences above threshold]
        # tempDict = defaultdict(int);
        # for e in nbrP:
        #     tempDict[int(e)] += 1
        # for k,v in tempDict.items():
        #     if v >= threshold:
        #         print person[0], k, v



    print "Finished successfully"

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

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
        for x,y in it.combinations(persons, 2):     #Evtl direkt printen?
            if y != None:
                edgelist[frozenset((x,y))] +=1
    print "Done."
    print "Printing the Edgelist"
    for edge in edgelist.items():
        if edgelist[edge[0]]>=threshold:
            for p in edge[0]:
                print p,
            print edge[1]

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

def secondMulti(graph):
    print "No. of Topics %d"%(len(graph.items()))
    for topic, persons in graph.items():
        templist = []
        for x, y in it.combinations(persons, 2):
            templist.append((x,y))
        print "T %d, combinations %d"%(topic, len(templist))
        # c = 0
        # for x,y in it.combinations(persons, 2):
        #     #print "%d %d"%(x,y)
        #     c += 1
        # print "T %d, count %d"%(topic, c)


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

def printDict(dict):
    for e in dict.items():
        print e

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

def buildUndirectedSnap():
    if args.verbose:
        print "Building undirected graph from",inputfile
    G1 = snap.LoadEdgeList(snap.PUNGraph, inputfile, 0, 1)
    if args.verbose:
        print "Done."
    return G1

def buildDirectedDict(inputfile):
    undirected = defaultdict(list);
    with open(inputfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        print "Buildung up the main dictionary",
        for key, value in reader:
            undirected[int(key)].append(int(value))
        print "\nDictionary built successfully!"
        return undirected

def buildUndirectedDict(inputfile):
    undirected = defaultdict(list);
    with open(inputfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        print "Buildung up the main dictionary",
        for key, value in reader:
            if not (int(value) in undirected[int(key)]):
                undirected[int(key)].append(int(value))
            if not (int(key) in undirected[int(value)]):
                undirected[int(value)].append(int(key))
        print "\nDictionary built successfully!"
        return undirected

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