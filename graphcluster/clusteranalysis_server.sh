input="$1"
awkscripts="$2"
cleanclustering="$awkscripts""cleanclustering.awk"
pythonscripts="$3"
analyseclustersscript="$pythonscripts""analyseclusters.py"

awk -f $cleanclustering $input | 
python -u $analyseclustersscript

