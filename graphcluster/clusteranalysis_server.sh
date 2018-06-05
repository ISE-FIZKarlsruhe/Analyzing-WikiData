louvainoutput="$1"
awkscripts="$2"
cleanclustering="$awkscripts""cleanclustering2.awk"
pythonscripts="$3"
analyseclustersscript="$pythonscripts""analyseclusters2.py"
labels="$4"

#
awk -f $cleanclustering2 $louvainoutput | 
sort -r -V -t ";" -k 2  > louvain_clean_names
python -u $analyseclustersscript louvain_clean_names criteriongraph.csv $labels
 
