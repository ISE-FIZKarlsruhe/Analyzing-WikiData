louvainoutput="$1"
awkscripts="$2"
cleanclustering="$awkscripts""cleanclustering.awk"
pythonscripts="$3"
analyseclustersscript="$pythonscripts""analyseclusters.py"

awk -f $cleanclustering $louvainoutput | 
sort -r -V -t ";" -k 1  > louvain_clean
python -u $analyseclustersscript louvain_clean

