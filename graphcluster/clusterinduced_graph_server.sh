awkscripts="$1"
printclutermembers="$awkscripts""printclustermembers.awk"
inputfile="$2" #louvainoutput unclean
clusternumber="$3"
overlapgraph="$4"
sed 's/\r//' $inputfile | grep "Partition $clusternumber" ../../project_germans/t0.75/louvainoutput_example | awk -f $printclutermembers > $clusternumber"Member"
cat <(join -1 1 -2 1 -t';' -o 1.1,1.2,1.3 <(sort -k1 -t';' $overlapgraph) <(sort $clusternumber"Member")) <(join -1 2 -2 1 -t';' -o 1.1,1.2,1.3 <(sort -k1 -t';' $overlapgraph) <(sort $clusternumber"Member")) | uniq > $clusternumber"induced_graph"