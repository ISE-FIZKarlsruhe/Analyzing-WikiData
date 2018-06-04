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
#inputfile = "wikidata_objects.txt"
#inputfile = "../results/wikidata_supertypeGraph.txt"
#inputfile = "../../WikiData/py/smallgraph4.txt"
inputfile = "../project_germans/t4/overlapgraph.txt"
#inputfile = "../project_germans/t4/sg7_overlapgraph_w.txt"
#inputfile = "smallgraph4.txt"                       #Server
#inputfile = "../results/wikidata_objects.txt"       #Server
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile. Must be a two column .txt", default=inputfile, action="store")
#parser.add_argument("--threshold","-t", type=int, nargs='?', help="threshold defining the minimal overlap for two persons to get an edge", default=4, action="store")
parser.add_argument("--directed", "-d", help="if the graph should be directed", action="store_true")
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
args = parser.parse_args()
inputfile = args.file


def main():
    Rnd = snap.TRnd(42)
    Rnd.Randomize()
    print "main"

### Basic methods
    ###
    #snap.PrintInfo(G1, "QA Stats", "qa-info.txt", False)
    #printEdges()
    #printDegrees()
    #print snap.GetBfsFullDiam(G1, 1000, True)
    #print 'IsConnected?', snap.IsConnected(G1)
    #print 'Weakly connected?', snap.IsWeaklyConn(G1)
    #WeakConnectedCompDistribution()
    #StrongConnectedCompDistribution()
    #WeakConnectedCompDistribution()
    print("")
    #getWeaklyConnectedComponents()
    #getMaxWcc()
    #getStronglyConnectedComponents()
    #print snap.GetMxInDegNId(G1)
    #print snap.CntDegNodes(G1, 5138062)
    #Plot Shortest Path Distribution
    #Graph = snap.GenRndGnm(snap.PNGraph, 100, 1000)
    #snap.PlotShortPathDistr(Graph, "example", "Directed graph - shortest path")

#Searches Maximal Closeness centrality.. Currently still takes way too long
    print "Max Closeness Path:"
    maxCCNode,maxCloseness = getMaxClosenessGreedy(G1.GetRndNId(Rnd))
    print "-----------"
    print "Highest Closeness Centrality: Node %d, Value %f" %(maxCCNode, maxCloseness)

#Returns the Closeness value for every node in the graph
    #for NI in G1.Nodes():
    #   print "node: %d, closeness %f" % (NI.GetId(), snap.GetClosenessCentr(G1, NI.GetId(), True, True))

###Print Nodes with OutDegree = 0
    #for NI in G1.Nodes():
    #    if NI.GetOutDeg() == 0:
    #        print NI.GetId()

#Returns the number of Triads within the graph
    #NumTriads = snap.GetTriads(G1, 50000)       #returns 66395
    #print 'Number of triads : %d' % NumTriads


###Print Cluster coefficients for every Node
    #for NI in G1.Nodes():
    #    print "node: %d, - cluster coefficient %f" % ( NI.GetId(), snap.GetNodeClustCf(G1, NI.GetId()))
    #print
    
    #negative clustercoefficients:
    # node: 1321, - cluster coefficient -0.000094
    # node: 1860, - cluster coefficient -0.001671

###Plot Degree Distribution
    #snap.PlotInDegDistr(G1,"degreeplot","Undirected Graph - in-degree Distribution")

    #printEdges()
    #removeZeroDegGreedy()
    #print("-----now:")
    #printEdges()


#Warning: modifies the original graph G1!
def removeZeroDegGreedy():
    removed = True;
    i = 0
    while removed == True:
        removed = False
        i += 1
        print i,"interation:"
        view = 0
        rem = 0
        for NI in G1.Nodes():
            view += 1
            stdout.write("\r%d" % view)
            stdout.flush()
            if NI.GetOutDeg() == 0 or NI.GetInDeg() == 0:
                toBeRemoved = snap.TIntV()
                toBeRemoved.Add(NI.GetId())
                snap.DelNodes(G1,toBeRemoved)
                removed = True
                rem += 1
        print "---removing:",rem

def buildDirected():
    print "Building directed graph from",inputfile
    G1 = snap.LoadEdgeList(snap.PNGraph, inputfile, 0, 1)
    print "Done."
    return G1

def buildUndirected():
    print "Building undirected graph from",inputfile
    G1 = snap.LoadEdgeList(snap.PUNGraph, inputfile, 0, 1)
    print "Done."
    return G1

def getNeighbors(nodeId):
    neighbors = snap.TIntV()
    node = G1.GetNI(nodeId)
    deg = node.GetInDeg()
    for i in range(0, deg):
        neighbors.Add(node.GetNbrNId(i))
    return deg, neighbors


def getMaxCloseness(startNodeId,verbose = True,isDir=True):
    checked = defaultdict(int);
    current = startNodeId
    checked[current] = 1
    currentCC = snap.GetClosenessCentr(G1, current, True, isDir)
    found = False
    while not found:
        deg,neighbors = getNeighbors(current)
        if verbose:
            print "Current Node: %d, Closeness: %f, Neighbors: %d" %(current,currentCC,deg)
        maxncc = 0
        maxneighbor = 0
        progress = 0
        for neighbor in neighbors:
            if verbose:
                progress += 1
                perc = (progress/deg)*100
                stdout.write("\r%f" % perc + "% ")
                stdout.flush()
            if checked[neighbor] == 0:
                checked[neighbor] = 1
                ncc = snap.GetClosenessCentr(G1, neighbor, True, isDir)
                if ncc > maxncc:
                    maxncc = ncc
                    maxneighbor = neighbor
        if verbose:
            print
        if maxncc <= currentCC:
            found = True
            return current, currentCC
        currentCC = maxncc
        current = maxneighbor

#Greedy version hops the the first node it finds that has a higher closeness centrality
def getMaxClosenessGreedy(startNodeId,verbose = True,isDir=True):
    checked = defaultdict(int);
    current = startNodeId
    checked[current] = 1
    currentCC = snap.GetClosenessCentr(G1, current, True, isDir)
    found = False

    while not found:
        breaked = False
        deg,neighbors = getNeighbors(current)
        if verbose:
            print "Current Node: %d, Closeness: %f, Neighbors: %d" %(current,currentCC,deg)
        maxncc = 0
        maxneighbor = 0
        progress = 0
        for neighbor in neighbors:
            if verbose:
                progress += 1
                stdout.write("\r%d" % progress + " neighbors viewed")
                stdout.flush()
            if checked[neighbor] == 0:
                checked[neighbor] = 1
                ncc = snap.GetClosenessCentr(G1, neighbor, True, isDir)
                if ncc > maxncc:
                    maxncc = ncc
                    maxneighbor = neighbor
                if ncc > currentCC:
                    breaked = True
                    break
        if verbose:
            print
        if maxncc <= currentCC and not breaked:
            found = True
            return current, currentCC
        currentCC = maxncc
        current = maxneighbor



def printEdges():
    for NI in G1.Nodes():
        for Id in NI.GetOutEdges():
            print "edge (%d %d)" % (NI.GetId(), Id)

def printDegrees():
    for NI in G1.Nodes():
        print "node: %d, out-degree %d, in-degree %d" % (NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())

def getStronglyConnectedComponents():
    Components = snap.TCnComV()
    snap.GetSccs(G1, Components)
    for i,CnCom in enumerate(Components):
        nodes = []
        if CnCom.Len() <= 50:
            for e in CnCom:
                nodes.append(e)
        else:
            nodes.append(CnCom[0])
        print "Component %d: Size: %d Member:" % (i+1,CnCom.Len()),nodes


def getMaxWcc():
    print("Members of largest weakly connected component")
    MxWcc = snap.GetMxWcc(G1)
    for EI in MxWcc.Nodes():
        print EI.GetId()


def getWeaklyConnectedComponents():
    print "getWeaklyConnectedComponents"
    Components = snap.TCnComV()
    snap.GetWccs(G1, Components)
    for i,CnCom in enumerate(Components):
        nodes = []
        if CnCom.Len() <= 50:
            for e in CnCom:
                nodes.append(e)
        else:
            nodes.append(CnCom[0])
        print "Component %d: Size: %d Member:" % (i+1,CnCom.Len()),nodes

def StrongConnectedCompDistribution():
    ComponentDist = snap.TIntPrV()
    snap.GetSccSzCnt(G1, ComponentDist)
    for comp in ComponentDist:
        print "ComponentSize: %d - Number of such Components: %d" % (comp.GetVal1(), comp.GetVal2())

def WeakConnectedCompDistribution():
    print "WeakConnectedCompDistribution"
    ComponentDist = snap.TIntPrV()
    snap.GetWccSzCnt(G1, ComponentDist)
    for comp in ComponentDist:
        print "ComponentSize: %d - Number of such Components: %d" % (comp.GetVal1(), comp.GetVal2())

if args.directed:
    G1 = buildDirected()
else:
    G1 = buildUndirected()
main()
