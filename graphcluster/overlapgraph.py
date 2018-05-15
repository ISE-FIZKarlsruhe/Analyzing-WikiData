#!/usr/bin/env python
from __future__ import division
import numpy as np
import csv
from collections import defaultdict
import argparse
import pandas as pd
from multiprocessing import Pool, Value, Lock
import functools

### INFO ###
#running on python 3.5
#inputfile is .csv

####File parameter
#----------------------------------------------------------------
inputfile = "../results/humangraph.csv"
inputfile = "../results/humangraph_germans_nt3.csv"
inputfile = "../py/smallgraph5.csv"
inputfile = "../../shell/smallgraph7_who.csv"
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile. Must be a two column .csv", default=inputfile, action="store")
#parser.add_argument("--threshold","-t", type=int, nargs='?', help="threshold defining the minimal overlap for two persons to get an edge", default=4, action="store")
parser.add_argument("--threshold","-t", type=int, nargs='?', help="threshold defining the minimal avg percentage overlap between two persons to get an edge", default=0.1, action="store")
parser.add_argument("--poolsize","-p", type=int, nargs='?', help="number of threads to run the program", default=4, action="store")
parser.add_argument("--weights", "-w", help="return a weight for each edge instead of just a binary decision", action="store_true")
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
args = parser.parse_args()
inputfile = args.file
if args.verbose:
    print("Inputfile:",inputfile)
threshold = args.threshold
poolsize = args.poolsize
args.weights = True

def main(threshold,poolsize):
    G1, auxdict = buildDictionaries(inputfile)
    edgelist = pd.read_csv(inputfile, sep=";", header=None)
    threshold = threshold
    pool = Pool(poolsize)
    if args.weights:
        pool.map(functools.partial(getConnectedPersonsWeighted, auxdict=auxdict, edgelist=edgelist, threshold=threshold, adjacency = G1), G1.items())
    else:
        pool.map(functools.partial(getConnectedPersons, auxdict=auxdict, edgelist=edgelist, threshold=threshold),
                 G1.items())
    pool.close()
    pool.join()

    ## single threaded
    # for person in G1.items():
    #     n += 1
    #     print "\n======= Person", n
    #     getConnectedPersons(person, threshold)

    print("Finished successfully")


def getConnectedPersons(person, auxdict, edgelist, threshold, adjacency):
    #print "--------------- Q%s\n" %(person[0]),
    #print auxdict[person[0]]
    pEdgelist = edgelist[auxdict[person[0]]:]
    #print pEdgelist
    nbrP = np.array(pEdgelist.loc[pEdgelist[1].isin(person[1])][0].values)
    #print nbrP

    ##method 1 - with threshold but no edge weight
    #outputstring
    output = ""
    # zuletzt ausgegebene Zahl
    lastprint = 0
    # wenn liste nicht leer
    if nbrP.any():
        current = nbrP[0]
    i = 0
    while i + threshold - 1 < len(nbrP):
        prev = current
        i += threshold - 1
        current = nbrP[i]
        if current == prev and current != lastprint:
            output += '%s;%s\n' % (person[0], current)
            lastprint = current
        else:
            for j in range(i - 1, (i - threshold), -1):
                if nbrP[j] != current:
                    i = j + 1
                    break
    print(output)

def getConnectedPersonsWeighted(person, auxdict, edgelist, threshold, adjacency):
    # print "--------------- Q%s\n" %(person[0]),
    # print auxdict[person[0]]
    pEdgelist = edgelist[auxdict[person[0]]:]
    # print pEdgelist
    nbrP = np.array(pEdgelist.loc[pEdgelist[1].isin(person[1])][0].values)
    # print nbrP

    ##Method 2 - full nested loop. But with edgelweights
    output = ""
    d = 0
    c = 0
    for e in nbrP:
        if e == d:
            c = c + 1
        else:
            score = round((c / len(adjacency[str(d)]) + c / len(person[1])) / 2, 4) if d != 0 else 0
            if score >= threshold:
                output += '%s;%s;%s\n' % (person[0], d, score)

            ## old threshold
            # if c >= threshold:
            #     score = round((c / len(adjacency[str(d)]) + c / len(person[1])) / 2, 4)
            #     output += '%s;%s;%s\n' % (person[0], d, score)

            d = e
            c = 1
    score = round((c / len(adjacency[str(d)]) + c / len(person[1])) / 2, 4) if d != 0 else 0
    if score >= threshold:
        output += '%s;%s;%s\n' % (person[0], d, score)
    print(output)


def buildDictionaries(inputfile):
    directed = defaultdict(list)
    auxdict = defaultdict(int)
    prevkey = 0
    line = 0
    key = 0

    with open(inputfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        print("Buildung up the main dictionary",end="")


        for key, value in reader:
            directed[key].append(value)
            if key != prevkey:
                auxdict[prevkey] = line
            prevkey = key
            line += 1
        auxdict[key] = line
        print("\nDone.")
        return directed, auxdict

if __name__ == '__main__':
    main(threshold, poolsize)



