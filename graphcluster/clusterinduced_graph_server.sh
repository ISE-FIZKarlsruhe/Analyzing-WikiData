awkscripts="$1"
printclustermembers="$awkscripts""printclustermembers.awk"
inputfile="$2" #louvainoutput unclean
clusternumber="$3"
overlapgraph="$4"
grep "Partition $clusternumber:" $inputfile | awk -f $printclustermembers > $clusternumber"Member"
cat <(LOCALE=C join -1 1 -2 1 -t';' -o 1.1,1.2 <(LOCALE=C sort -k1 -t';' $overlapgraph) <(LOCALE=C sort $clusternumber"Member")) <(LOCALE=C join -1 2 -2 1 -t';' -o 1.1,1.2 <(LOCALE=C sort -k2 -t';' $overlapgraph) <(LOCALE=C sort $clusternumber"Member")) | uniq > $clusternumber"induced_graph"