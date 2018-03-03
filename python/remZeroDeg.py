#!/usr/bin/env python

import pandas as pd
import argparse


####File parameter
#----------------------------------------------------------------
#defaults
inputfile = "no file"
inputfile = "../results/wikidata_supertypeGraph.csv"
#parser
parser = argparse.ArgumentParser()
parser.add_argument('inputfile', type=str, nargs='?', help="specifies the inputfile", default=inputfile, action="store")
parser.add_argument('--outfile',"-o", type=str, nargs='?', help="specifies the outputfile (no .csv needed)", default="no file", action="store")
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
args = parser.parse_args()
inputfile = args.inputfile
outputfile = args.outfile+".csv"
print("Inputfile:",inputfile)
print("Outputfile:",outputfile)
print()

def main():
    graph = buildDirected(inputfile)
    graph = removeZeroDeg(graph)

    if outputfile == "no file":
        print(graph.to_string(index=False, index_names=False))
    else:
        graph.to_csv(outputfile,sep=";",index=False, header=False)
        print("sucess")


def removeZeroDeg(graph):
    i = 0;
    removed = True
    while removed == True:
        i += 1
        if args.verbose:
            print(i, "interation:")
        size_bef = graph.shape[0]
        graph = graph.loc[graph['0'].isin(graph['1'])]
        graph = graph.loc[graph['1'].isin(graph['0'])]
        size_aft = graph.shape[0]
        if args.verbose:
            print("---removing:", size_bef - size_aft)
        removed = (size_bef != size_aft)
    return graph

def buildDirected(inputfile):
    graph = pd.read_csv(inputfile, sep=";",names = ["0","1"])
    return graph

main()
