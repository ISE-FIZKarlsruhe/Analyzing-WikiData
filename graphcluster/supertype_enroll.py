#!/usr/bin/env python
import numpy as np
import csv
from collections import defaultdict
import argparse
import pandas as pd
import operator
import networkx as nx
from collections import Counter


####File parameter
#----------------------------------------------------------------
inputfile_supertypegraph = "../results/wikidata_supertypeGraph_noqual.csv"
inputfile_labels = "../results/labels_english"
parser = argparse.ArgumentParser()
parser.add_argument('supertype_file', type=str, nargs='?', help="specifies the cluster inputfile. Must be .csv with a list of clustermembers in each row.", default=inputfile_supertypegraph, action="store")
parser.add_argument('labels_file', type=str, nargs='?', help="specifies the label inputfile. Must be a two column .txt. Label ist seperated from reference number by space.", default=inputfile_labels, action="store")
parser.add_argument('concept', type=int, nargs='?', help="specifies the concept all printet entities will belong to.", default=4830453, action="store")
parser.add_argument("--lowestlevel", "-l", help="prints only the leaf nodes of the given concept tree", action="store_true")
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
args = parser.parse_args()
inputfile_supertypegraph = args.supertype_file
inputfile_labels = args.labels_file

start = args.concept

#inputfile = "../py/smallgraph8.csv"
#start = 7

i = 0

def main():
    if args.lowestlevel:
        printLowestLevel(start)
        print("------")
        print(i)
    else:
        printAllLevels(start, 0)


def printLowestLevel(node):
    global i
    if Graph.get(node) == None:
        print(node)
        i +=1
        return
    for subtype in Graph.get(node):
        printLowestLevel(subtype)



def printAllLevels(node, level):
    if Graph.get(node) == None:
        return
    for subtype in Graph.get(node):
        if args.verbose:
            print("---"*level,subtype,Labels.get(str(subtype)))
        else:
            print(subtype)
        printAllLevels(subtype, level+1)



def buildLabelDict(inputfile):
    labeldict = defaultdict()
    #print("Building up labeldictionary", end=" ")
    with open(inputfile, encoding="utf8") as labelfile:
        for line in labelfile:
            number, text = line.split(' ', maxsplit=1)
            text = text[:-1]
            labeldict[number] = text
    #print("\nDictionary built successfully!\n")
    return labeldict


def buildReversed(inputfile):
    dictionary = defaultdict(list);
    i = 0;
    #print("Building up dictionary", end=" ")
    with open(inputfile, newline ='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for key, value in reader:
            dictionary[int(value)].append(int(key))
    #print("\nDictionary built successfully!\n")
    return dictionary

Graph = buildReversed(inputfile_supertypegraph)
if args.verbose:
    Labels = buildLabelDict(inputfile_labels)
main()