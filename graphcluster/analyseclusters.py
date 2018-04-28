#!/usr/bin/env python
import numpy as np
import csv
from collections import defaultdict
import argparse
import pandas as pd
import operator

### INFO ###
#running on python 3.5
#inputfile is .csv

####File parameter
#----------------------------------------------------------------
inputfile_clusters = "../py/smallclusters.csv"
inputfile_edgelist = "../results/humangraph.csv"
inputfile_labels = "../results/labels_english"
parser = argparse.ArgumentParser()
parser.add_argument('cluster_file', type=str, nargs='?', help="specifies the cluster inputfile. Must be .csv with a list of clustermembers in each row.", default=inputfile_clusters, action="store")
parser.add_argument('edgelist_file', type=str, nargs='?', help="specifies the edgelist inputfile. Must be a two column .csv containing specific entities on the left and their 'objects' on the right.", default=inputfile_edgelist, action="store")
parser.add_argument('labels_file', type=str, nargs='?', help="specifies the label inputfile. Must be a two column .csv containing specific entities on the left and their 'objects' on the right.", default=inputfile_labels, action="store")
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
args = parser.parse_args()
inputfile_clusters = args.cluster_file
inputfile_edgelist = args.edgelist_file
inputfile_labels = args.labels_file
if args.verbose:
    print("Inputfile_cluster:",inputfile_clusters)
    print("Inputfile_edgelist:", inputfile_edgelist)
    print("Inputfile_labels:", inputfile_labels)
labelfile_delimiter = "EcmLIJ6vTW6 "

def main():
    print("Loading edgelist...")
    edgelist = pd.read_csv(inputfile_edgelist, sep=";", header=None)
    print("Building labelgraph...")
    labeldict = defaultdict()
    with open(inputfile_labels, encoding="utf8") as labelfile:
        for line in labelfile:
            number, text = line.split(' ', maxsplit=1)
            text = text[:-1]
            labeldict[number] = text
        #labeldict = dict([line.split(' ', maxsplit=1) for line in labelfile])


    #labels = pd.DataFrame.from_records(data, columns=['Integer', 'String'])
    #labels = pd.read_csv(inputfile_labels, sep=labelfile_delimiter, header=None, engine='python')


    with open(inputfile_clusters) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        linenumber = 0
        for line in reader:
            linenumber += 1
            attcount = defaultdict(int)
            cluster = np.array(line)
            all_attributes = np.array(edgelist.loc[edgelist[0].isin(cluster)][1].values)
            for e in all_attributes:
                attcount[e] += 1

            sorted_attcount = sorted(attcount.items(), key=operator.itemgetter(1), reverse=True)

            #old approach
            # print("\nCluster %d: Attributes:"%(linenumber),end=" ")
            # freq_attribute = []
            # freq_attribute_numbers = []
            # for attribute, count in sorted_attcount[:5]:
            #     freq_attribute.append(attribute)
            #     freq_attribute_numbers.append(tuple((attribute, str("%.2f" % round(count / len(cluster)*100,2)+"%"))))
            # print(freq_attribute_numbers)
            # names = labels.loc[labels[0].isin(freq_attribute)][1].tolist()
            # print("Cluster %d: Attributes:" % (linenumber), end=" ")
            # print(names)
            # if len(names) < len(freq_attribute):
            #     print(len(freq_attribute)-len(names)," label(s) not found!")

            print("\nCluster %d:"%(linenumber))
            freq_attribute = []
            for attribute, count in sorted_attcount[:10]:
                #label = labeldict[str(attribute)] if str(attribute) in labeldict else "no label"
                label = labeldict.get(str(attribute))
                freq_attribute.append([attribute, label, str("%.2f" % round(count / len(cluster)*100,2)+"%")])
            for f in freq_attribute:
                print(f)






main()