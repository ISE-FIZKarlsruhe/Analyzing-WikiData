#!/usr/bin/env python
import numpy as np
import csv
from collections import defaultdict
import argparse
import pandas as pd
import operator
import networkx as nx
from collections import Counter

### INFO ###
#running on python 3.5
#inputfile is .csv

####File parameter
#----------------------------------------------------------------
inputfile_clusters = "../project_germans/t0.75/louvain_clean_names"
inputfile_edgelist = "../project_germans/t0.75/criteriongraph.csv"
inputfile_overlapgraph = "../project_germans/t0.75/overlapgraph_clean"
inputfile_labels = "../results/labels_english"
parser = argparse.ArgumentParser()
parser.add_argument('cluster_file', type=str, nargs='?', help="specifies the cluster inputfile. Must be .csv with a list of clustermembers in each row.", default=inputfile_clusters, action="store")
parser.add_argument('edgelist_file', type=str, nargs='?', help="specifies the edgelist inputfile. Must be a two column .csv containing specific entities on the left and their 'objects' on the right.", default=inputfile_edgelist, action="store")
parser.add_argument('labels_file', type=str, nargs='?', help="specifies the label inputfile. Must be a two column .txt. Label ist seperated from reference number by space.", default=inputfile_labels, action="store")
parser.add_argument('overlapgraph_file', type=str, nargs='?', help="specifies the overlapgraph inputfile", default=inputfile_overlapgraph, action="store")
parser.add_argument('threshold', type=int, nargs='?', help="specifies the threshold of cluster sizes. Only clusters with at least t members will be interpreted.", default=500, action="store")
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
parser.add_argument("--humanreadable", "-h", help="makes output readable for humans", action="store_true")
args = parser.parse_args()
inputfile_clusters = args.cluster_file
inputfile_edgelist = args.edgelist_file
inputfile_labels = args.labels_file
inputfile_overlapgraph = args.overlapgraph_file
if args.verbose:
    print("Inputfile_cluster:",inputfile_clusters)
    print("Inputfile_edgelist:", inputfile_edgelist)
    print("Inputfile_labels:", inputfile_labels)
    print("Inputfile_overlapgraph:", inputfile_overlapgraph)


def main():
    if args.verbose:
        print("Loading edgelist...")
    edgelist = pd.read_csv(inputfile_edgelist, sep=";", header=None)
    total_criterions = edgelist[0].nunique()

    if args.verbose:
        print("Loading overlapgraph...")
    overlapgraph = nx.read_edgelist(inputfile_overlapgraph, nodetype=int, delimiter=";", data=(('weight',float),))
    total_overlapgraph = len(overlapgraph.nodes())

    if args.verbose:
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

        total_incluster = []
        candidate_attributes = defaultdict(list)
        sizes = defaultdict(int)
        attribute_descriptions = defaultdict(list)
        nonparticipatings = defaultdict(float)
        coverages = defaultdict()
        max_coverage_members = defaultdict(float)
        top_pageranked = defaultdict(list)



        #Iterate over each line containg one Cluster.
        #Genereate a candidate attributeset for every Cluster/Line
        for line in reader:

            linenumber += 1
            attcount = defaultdict(int)
            cluster_id = int(line[0])
            cluster_size = int(line[1])
            cluster_members = np.array(line[2:])

            if int(cluster_size) >= cluster_threshold:
                if args.verbose:
                    print("\rAnalyzing Cluster", cluster_id)
                total_incluster += list(map(int, cluster_members))

                ##PageRank
                membergraph = overlapgraph.subgraph(list(map(int,cluster_members)))
                pr = nx.pagerank(membergraph, alpha=0.85)
                top_pageranked[cluster_id] = [x[0] for x in sorted(pr.items(), key=operator.itemgetter(1), reverse=True)[:5]]

                ##ATTRIBUTES
                #get the attributes (i.e. the objects all members of the cluster link to)
                sizes[cluster_id] = cluster_size

                #new
                cluster_edgelist = edgelist.loc[edgelist[0].isin(cluster_members)]
                all_attributes_and_predicates = cluster_edgelist[[1,2]]
                all_attributes = np.array(all_attributes_and_predicates[2].values)


                #rank all alltributes of this cluster by frequency
                for e in all_attributes:
                    attcount[e] += 1
                sorted_attcount = sorted(attcount.items(), key=operator.itemgetter(1), reverse=True)[:25]

                #append the 25 most frequent attributes to the current clusters candidates dictionary (i.e. the clustering)
                for attribute, count in sorted_attcount:

                    #for the current attribute - get the list of all its predictes and rank the predicate according to their frequency
                    top_predicates = sorted(Counter(all_attributes_and_predicates.loc[all_attributes_and_predicates[2]== attribute][1].values).items(),key=operator.itemgetter(1), reverse=True)[:5]
                    top_predicates = [str(p) + " " + str(int((c/count)*100)) + "%" for p, c in top_predicates]
                    top_predicates = "Predicates: P" + ", P".join(top_predicates)

                    candidate_attributes[cluster_id].append((int(attribute), round(count / len(cluster_members)*100,2), top_predicates))
                    #save the aggregated (sum) information on the attribute frequency in a seperate dict
                    attributes_aggregated[int(attribute)] += round(count / len(cluster_members)*100,2)

                ##PARTICIPATION and COVERAGE
                #Calculate percentage of Members of this cluster who do not link to any of the top 25 'attributes'
                nonparticipating = 0
                nonparticipating_threshold = 2
                coverage = 0
                max_coverage = 0
                max_covering_entitites = []
                for member in cluster_members:
                    thismembers_attributes = np.array(edgelist.loc[edgelist[0]==int(member)][2].values)
                    intersect_with_frequent=np.intersect1d(thismembers_attributes,sorted_attcount)
                    covers = len(intersect_with_frequent)
                    if len(intersect_with_frequent) < nonparticipating_threshold:
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
        n = len(candidate_attributes.keys())   #how many clusters are there

###Generating metainformation/results
        print("Generating results...")
        #Generate the calculated information for each candidate attribute and sord the candidate attributes by their score value
        for this_cluster in candidate_attributes.items():
            for candidate in this_cluster[1]:
                #set the uniquesness marker to '1' if the currently viewed cluster has all occurences of the viewed attribute
                unique = 1 if attributes_aggregated[int(candidate[0])]-candidate[1]==0 else 0
                score = round(candidate[1] - ((attributes_aggregated[int(candidate[0])]-candidate[1])/(n-1)),2)

                attribute_descriptions[this_cluster[0]].append((candidate[0], labeldict.get(str(candidate[0])), candidate[1], score, unique, candidate[2]))
                #attribute_descriptions[this_cluster[0]].append((candidate[0], candidate[1], score ,unique, candidate[2])) #nolabel

            attribute_descriptions[this_cluster[0]].sort(key=lambda tup: tup[3], reverse=True)

        #Converting and sorting the size values to easy interpretation and correct iteration
        sizes_df = pd.Series(list(sizes.values()))
        sorted_sizes = sorted(sizes.items(), key=operator.itemgetter(1),reverse=True)

###PRINTING RESULTS
		if args.humanreadable:
	        print("\n_____________________\nClustering Metainformation:")
	        print("No. of Persons with criterion: %d" % (total_criterions))
	        print("No. of Persons in overlapgraph: %d" % (total_overlapgraph))
	        print("No. of Persons in clustering: %d" % (len(set(total_incluster))))

	        print("Cluster count %d" % (int(sizes_df.count())))
	        print("Avg cluster size %d" % (int(sizes_df.mean())))
	        print("Cluster size std %d" % (int(sizes_df.std())))
	        print("Cluster size variance %d" %(int(sizes_df.var())))
	        print("Avg nonparticipating %d" % (int(np.array(list(nonparticipatings.values())).sum()/sizes_df.count())))
	        avg_cluster_coverage = 0
	        for c in coverages.values():
	            avg_cluster_coverage += c[0]
	        print("avg coverage %f" % (avg_cluster_coverage / sizes_df.count()))

	        print("\n_____________________\nSpecific clusters ordered by size:")
	        for id,size in sorted_sizes:
	            print("\nCluster No. %d Members: %d Nonparticipating: %d Avg_Coverage: %f, Max_Coverage: %d" %(id, size, nonparticipatings[id],coverages[id][0],coverages[id][1]))
	            print("Max Coverage Members:",max_coverage_members[id])
	            print("Top 5 PageRank Members:", top_pageranked[id])
	            for attribute in attribute_descriptions[id]:
	                print(attribute)


main()