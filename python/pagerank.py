#!/usr/bin/env python
import numpy as np
import csv
from collections import defaultdict
import argparse
import pandas as pd
import operator
import networkx as nx
from collections import Counter

inputfile_wikidata = "../py/smallgraph7.csv"
parser = argparse.ArgumentParser()
parser.add_argument('wikidata_file', type=str, nargs='?', help="specifies the full wikidata graph inputfile", default=inputfile_wikidata, action="store")
args = parser.parse_args()
inputfile_wikidata = args.wikidata_file

print("Loading overlapgraph...")
wikidatagraph = nx.read_edgelist(inputfile_wikidata, nodetype=int, delimiter=";")
pr = nx.pagerank(wikidatagraph, alpha=0.85)
for key, value in pr.items():
    print(str(key)+";"+str(value))