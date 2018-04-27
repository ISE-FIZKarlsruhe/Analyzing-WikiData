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
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile. Must be a two column .csv", default=inputfile, action="store")
parser.add_argument("--threshold","-t", type=int, nargs='?', help="threshold defining the minimal overlap for two persons to get an edge", default=2, action="store")
parser.add_argument("--poolsize","-p", type=int, nargs='?', help="number of threads to run the program", default=4, action="store")
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
args = parser.parse_args()
inputfile = args.file
if args.verbose:
    print("Inputfile:",inputfile)
threshold = args.threshold
poolsize = args.poolsize

def main(threshold,poolsize):
    G1, auxdict = buildDictionaries(inputfile)
    edgelist = pd.read_csv(inputfile, sep=";", header=None)
    threshold = threshold

    pool = Pool(poolsize)
    pool.map(functools.partial(getConnectedPersons, auxdict=auxdict, edgelist=edgelist, threshold=threshold), G1.items())
    pool.close()
    pool.join()

    ## single threaded
    # for person in G1.items():
    #     n += 1
    #     print "\n======= Person", n
    #     getConnectedPersons(person, threshold)

    print("Finished successfully")


def getConnectedPersons(person, auxdict, edgelist, threshold):
    #print "--------------- Q%s\n" %(person[0]),
    #print auxdict[person[0]]
    pEdgelist = edgelist[auxdict[person[0]]:]
    #print pEdgelist
    nbrP = np.array(pEdgelist.loc[pEdgelist[1].isin(person[1])][0].values)
    #print nbrP

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


def buildDictionaries(inputfile):
    directed = defaultdict(list)
    auxdict = defaultdict(int)
    prevkey = 0
    line = 0

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

class Counter(object):
    def __init__(self, initval=0):
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value

if __name__ == '__main__':
    main(threshold, poolsize)



