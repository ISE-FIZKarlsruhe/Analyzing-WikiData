awkscripts="$1"
printclutermembers="$awkscripts""printclustermembers.awk"
inputfile="$2" #louvainoutput unclean
clusternumber="$3"
overlapgraph="$4"
grep "Partition $clusternumber:" $inputfile | awk -f $printclutermembers > $clusternumber"Member"
cat <(join -1 1 -2 1 -t';' -o 1.1,1.2,1.3 <(sort -k1 -t';' $overlapgraph) <(sort $clusternumber"Member")) <(join -1 2 -2 1 -t';' -o 1.1,1.2,1.3 <(sort -k2 -t';' $overlapgraph) <(sort $clusternumber"Member")) | uniq > $clusternumber"induced_graph"