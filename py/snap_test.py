#!/usr/bin/env python
import numpy as np
import csv
from collections import defaultdict
import snap

inputfile = "../../WikiData/py/wikidata_objects.txt"
inputfile = "../results/wikidata_typesubclass.txt"
#inputfile = "../../WikiData/py/smallgraph4.txt"
#inputfile = "smallgraph4.txt"                       #Server
#inputfile = "../results/wikidata_objects.txt"       #Server
directed = True

def main():
    print
    #snap.PrintInfo(G1, "QA Stats", "qa-info.txt", False)
    #printEdges()
    #printDegrees()
    #print snap.GetBfsFullDiam(G1, 1000, True)
    #print 'IsConnected?', snap.IsConnected(G1)
    #print 'Weakly connected?', snap.IsWeaklyConn(G1)
    #WeakConnectedCompDistribution()
    #getWeaklyConnectedComponents()
    #getConnectedComponents()
    #print snap.GetMxInDegNId(G1)
    #print snap.CntDegNodes(G1, 5138062)
    #Plot Shortest Path Distribution
    #Graph = snap.GenRndGnm(snap.PNGraph, 100, 1000)
    #snap.PlotShortPathDistr(Graph, "example", "Directed graph - shortest path")

    #Closeness
    #for NI in G1.Nodes():
    #    print "node: %d, closeness %f" % (NI.GetId(), snap.GetClosenessCentr(G1, NI.GetId(), True, True))

    for NI in G1.Nodes():
        if NI.GetOutDeg() == 0:
            print NI.GetId()
        
    #Triads
    #NumTriads = snap.GetTriads(G1, 50000)       #returns 66395
    #print 'Number of triads : %d' % NumTriads

    #Cluster coefficients
    #for NI in G1.Nodes():
    #    print "node: %d, - cluster coefficient %f" % ( NI.GetId(), snap.GetNodeClustCf(G1, NI.GetId()))
    #print
    
    #negative clustercoefficients:
    # node: 1321, - cluster coefficient -0.000094
    # node: 1860, - cluster coefficient -0.001671

    #Plot Degree Distribution
    #snap.PlotInDegDistr(G1,"degreeplot","Undirected Graph - in-degree Distribution")

def buildDirected():
    G1 = snap.LoadEdgeList(snap.PNGraph, inputfile, 0, 1)
    return G1

def buildUndirected():
    G1 = snap.LoadEdgeList(snap.PUNGraph, inputfile, 0, 1)
    return G1

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
        if CnCom.Len() <= 5:
            for e in CnCom:
                nodes.append(e)
        else:
            nodes.append(CnCom[0])
        print "Component %d: Size: %d Member:" % (i+1,CnCom.Len()),nodes

def getWeaklyConnectedComponents():
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
    ComponentDist = snap.TIntPrV()
    snap.GetWccSzCnt(G1, ComponentDist)
    for comp in ComponentDist:
        print "ComponentSize: %d - Number of such Components: %d" % (comp.GetVal1(), comp.GetVal2())

if directed:
    G1 = buildDirected()
else:
    G1 = buildUndirected()
main()
