awkscripts="$1"
humanwhoscript="$awkscripts""humangraphwho3.awk"
wikidata="$2wikidata_undirected"
pythonscripts="$3"
overlapgraphscript="$pythonscripts""overlapgraph.py"
criterion="$4"
threshold="$5"

poolsize=16

removetrivial='BEGIN{FS=";"}{if($2!=5&&$2!='$criterion')print$0}'
awk -v c=$criterion -f $humanwhoscript $wikidata | awk $removetrivial > criteriongraph.csv
python -u $overlapgraphscript -w -t $threshold -p $poolsize criteriongraph.csv

