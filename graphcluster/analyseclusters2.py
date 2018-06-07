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

        candidates = defaultdict(list)
        sizes = defaultdict(int)
        description = defaultdict(list)
        nonparticipatings = defaultdict(float)
        coverages = defaultdict()
        max_coverage_members = defaultdict(float)



        #Iterate over each line containg one Cluster.
        #Genereate a candidate attributeset for every Cluster/Line
        for line in reader:
            linenumber += 1
            attcount = defaultdict(int)
            cluster_id = int(line[0])
            cluster_size = int(line[1])
            cluster_members = np.array(line[2:])

            if int(cluster_size) > cluster_threshold:
                #get the attributes (i.e. the objects all members of the cluster link to)
                sizes[cluster_id] = cluster_size
                all_attributes = np.array(edgelist.loc[edgelist[0].isin(cluster_members)][1].values)
                #rank all alltributes of this cluster by frequency
                for e in all_attributes:
                    attcount[e] += 1
                sorted_attcount = sorted(attcount.items(), key=operator.itemgetter(1), reverse=True)[:25]

                #append the 25 most frequent attributes to the current clusters candidates dictionary (i.e. the clustering)
                for attribute, count in sorted_attcount:
                    candidates[cluster_id].append((int(attribute), round(count / len(cluster_members)*100,2)))
                    #save the aggregated (sum) information on the attribute frequency in a seperate dict
                    attributes_aggregated[int(attribute)] += round(count / len(cluster_members)*100,2)

                #Calculate percentage of Members of this cluster who do not link to any of the top 25 'attributes'
                nonparticipating = 0
                coverage = 0
                max_coverage = 0
                max_covering_entitites = []
                for member in cluster_members:
                    thismembers_attributes = np.array(edgelist.loc[edgelist[0]==int(member)][1].values)
                    intersect_with_frequent=np.intersect1d(thismembers_attributes,sorted_attcount)
                    covers = len(intersect_with_frequent)
                    if not intersect_with_frequent.any():
                        nonparticipating += 1
                    coverage += covers
                    if covers == max_coverage:
                        max_covering_entitites.append(member)
                    if covers > max_coverage:
                        max_covering_entitites = [member]
                        max_coverage = covers
                #nonparticipatings[cluster_id] = round(nonparticipating/cluster_size,5)
                coverages[cluster_id] = (coverage/cluster_size, max_coverage)
                nonparticipatings[cluster_id] = int(nonparticipating)
                max_coverage_members[cluster_id] = max_covering_entitites

        #get the number of clusters with a number of members above the threshold
        n = len(candidates.keys())   #how many clusters are there

        #Generate the calculated information for each candidate attribute and sord the candidate attributes by their score value
        for this_cluster in candidates.items():
            for candidate in this_cluster[1]:
                #set the uniquesness marker to '1' if the currently viewed cluster has all occurences of the viewed attribute
                unique = 1 if attributes_aggregated[int(candidate[0])]-candidate[1]==0 else 0
                description[this_cluster[0]].append((candidate[0], labeldict.get(str(candidate[0])), candidate[1], round(candidate[1] - ((attributes_aggregated[int(candidate[0])]-candidate[1])/(n-1)),2),unique))
                #description[this_cluster[0]].append((candidate[0], candidate[1], round(candidate[1] - ((attributes_aggregated[int(candidate[0])]-candidate[1])/(n-1)),2),unique)) #nolabel

            description[this_cluster[0]].sort(key=lambda tup: tup[3], reverse=True)

        #Converting and sorting the size values to easy interpretation and correct iteration
        sizes_df = pd.Series(list(sizes.values()))
        sorted_sizes = sorted(sizes.items(), key=operator.itemgetter(1),reverse=True)

###PRINTING RESULTS
        print("\n_____________________\nClustering Metainformation:")
        #print(sizes_df.describe()[['count','mean','std']].reset_index().to_csv(header=None, index=None, sep=' '))
        print("count %f" % (int(sizes_df.count())))
        print("size mean %f" % (int(sizes_df.mean())))
        print("size std %f" % (int(sizes_df.std())))
        print("size variance %f" %(int(sizes_df.var())))
        print("avg nonpart %f" % (np.array(list(nonparticipatings.values())).sum()/sizes_df.count()))
        avg_cluster_coverage = 0
        for c in coverages.values():
            avg_cluster_coverage += c[0]
        print("avg coverage %f" % (avg_cluster_coverage / sizes_df.count()))

        print("\n_____________________\nSpecific Cluster ordered by size:")
        for id,size in sorted_sizes:
            print("\nCluster No. %d Members: %d Nonparticipating: %d Avg_Coverage: %f, Max_Coverage: %d" %(id, size, nonparticipatings[id],coverages[id][0],coverages[id][1]))
            print("Max Coverage Members:",max_coverage_members[id])
            for attribute in description[id]:
                print(attribute)





main()