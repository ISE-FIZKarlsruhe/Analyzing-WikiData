#!/usr/bin/env python
import argparse
import numpy as np
from collections import defaultdict
import csv

#inputfile = "smallgraph4.csv"
inputfile = "wikidata_objects.csv"

def buidIndex(inputfile):
    nameindex = defaultdict(int);
    i = 0;
    with open(inputfile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        print("Buildung up index", end=" ")
        for key, value in reader:
            if not (int(key) in nameindex.keys()):
                nameindex[int(key)] = i
                i += 1
        print("\nIndex built successfully!\n")
        return nameindex, i

def buildAdjacencyMatrix(inputfile):
    nameindex, nodes = buidIndex(inputfile)
    adjacency = np.zeros(shape=(nodes, nodes))

    with open(inputfile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        print("Buildung up Matrix", end=" ")
        for key, value in reader:
            adjacency[nameindex.get(int(key)), nameindex.get(int(value))] = 1
            adjacency[nameindex.get(int(value)), nameindex.get(int(key))] = 1
        print("\nMatrix built successfully!\n")
        return adjacency, nodes


def isFullyConnected(inputfile):
    a, nodes = buildAdjacencyMatrix(inputfile)
    s = np.zeros(shape=(nodes, nodes))
    powertwomatrices = []
    powertwomatrices.append(a)
    print("Starting Matrix powering")
    for i in range(1, nodes):                       #i is like step or distance
        bitstringrev = '{0:b}'.format(i)[::-1]
        t = np.identity(nodes)
        for pos, bit in enumerate(bitstringrev):
            if int(bit) == 1:
                t = np.greater(np.dot(t,powertwomatrices[pos]),0)
        s = np.add(s, t)
        if (i & (i + 1)) == 0:
            powertwomatrices.append(np.dot(t, a))
        if not 0 in s:
            return True, i
    return False

print("Graph is fully connected?",isFullyConnected(inputfile))