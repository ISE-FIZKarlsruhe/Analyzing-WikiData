awkscripts="$1"
humanwhoscript="$awkscripts""humangraphwho4.awk"
wikidata="$2"
pythonscripts="$3"
overlapgraphscript="$pythonscripts""overlapgraph.py"
criterion="$4"
threshold="$5"

poolsize=16

removetrivial='BEGIN{FS=";"}{if($3!=5&&$3!='$criterion')print$0}'
awk -v c=$criterion -f $humanwhoscript $wikidata | awk $removetrivial | awk '!s[$0]++' > criteriongraph.csv
python -u $overlapgraphscript -w -t $threshold -p $poolsize criteriongraph.csv

