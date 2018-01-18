import numpy as np
import csv
from collections import defaultdict
import snap

inputfile = "../../WikiData/py/wikidata_objects.txt"
#inputfile = "../../WikiData/py/smallgraph4.txt"
rebuild = True

def main():
    print
    #printEdges()
    #printDegrees()
    #print snap.GetBfsFullDiam(G1, 1000, True)
    #print 'IsConnected?', snap.IsConnected(G1)
    #print 'Weakly?', snap.IsWeaklyConn(G1)
    #WeakConnectedCompDistribution()
    getWeaklyConnectedComponents()
    #getConnectedComponents()
    #print snap.GetMxInDegNId(G1)
    #print snap.CntDegNodes(G1, 5138062)
    #Plot Shortest Path Distribution
    #Graph = snap.GenRndGnm(snap.PNGraph, 100, 1000)
    #snap.PlotShortPathDistr(Graph, "example", "Directed graph - shortest path")

    #Closeness
    #for NI in G1.Nodes():
    #    print "node: %d, closeness %f" % (NI.GetId(), snap.GetClosenessCentr(G1, NI.GetId(), True, True))

    #S1 = snap.GetRndSubGraph(G1, 20)
    #for NI in S1.Nodes():
    #    print "node: %d, out-degree %d, in-degree %d" % ( NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
        


def buildDirected():
    G1 = snap.LoadEdgeList(snap.PNGraph, inputfile, 0, 1)
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

if rebuild:
    G1 = buildDirected()
main()
