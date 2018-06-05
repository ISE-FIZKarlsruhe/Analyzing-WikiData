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
parser.add_argument('labels_file', type=str, nargs='?', help="specifies the label inputfile. Must be a two column .txt. Label ist seperated from reference number by space.", default=inputfile_labels, action="store")
parser.add_argument('threshold', type=int, nargs='?', help="specifies the threshold of cluster sizes. Only clusters with at least t members will be interpreted.", default=500, action="store")
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

    print("Building label dictionary...")
    labeldict = defaultdict()
    with open(inputfile_labels, encoding="utf8") as labelfile:
        for line in labelfile:
            number, text = line.split(' ', maxsplit=1)
            text = text[:-1]
            labeldict[number] = text

    with open(inputfile_clusters) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        linenumber = 0
        cluster_threshold = args.threshold
        attributes_aggregated = defaultdict(float)

        clustering = defaultdict(list)
        sizes = defaultdict(int)
        description = defaultdict(list)

        #Iterate over each line containg one Cluster.
        #Genereate a candidate attributeset for every Cluster/Line
        for line in reader:
            linenumber += 1
            attcount = defaultdict(int)
            cluster_id = int(line[0])
            cluster_size = int(line[1])
            cluster_members = np.array(line[2:])
            
            if int(cluster_size) > cluster_threshold:
                sizes[cluster_id] = cluster_size
                all_attributes = np.array(edgelist.loc[edgelist[0].isin(cluster_members)][1].values)
                for e in all_attributes:
                    attcount[e] += 1
                sorted_attcount = sorted(attcount.items(), key=operator.itemgetter(1), reverse=True)

                #print("\nCluster No. %d: Size %d"%(cluster_id,int(cluster_size)))
                for attribute, count in sorted_attcount[:25]:
                    #label = labeldict[str(attribute)] if str(attribute) in labeldict else "no label"
                    #label = labeldict.get(str(attribute))
                    clustering[cluster_id].append((int(attribute), round(count / len(cluster_members)*100,2)))
                    attributes_aggregated[int(attribute)] += round(count / len(cluster_members)*100,2)

        n = len(clustering.keys())   #how many clusters are there

        for this_cluster in clustering.items():
            for candidate in this_cluster[1]:
                unique = 1 if attributes_aggregated[int(candidate[0])]-candidate[1]==0 else 0
                description[this_cluster[0]].append((candidate[0], labeldict.get(str(candidate[0])), candidate[1], candidate[1] - ((attributes_aggregated[int(candidate[0])]-candidate[1])/(n-1)),unique))
            description[this_cluster[0]].sort(key=lambda tup: tup[3], reverse=True)


        sorted_sizes = sorted(sizes.items(), key=operator.itemgetter(1),reverse=True)

        for id,size in sorted_sizes:
            print("\nCluster No.", id, " Members:", size)
            for attribute in description[id]:
                print(attribute)

        # for cluster in description.items():
        #     print("\nCluster No.",cluster[0], " Members:", sizes[cluster[0]])
        #     for attribute in cluster[1]:
        #         print(attribute)






main()