awkscripts="$1"
humanwhoscript="$awkscripts""humangraphwho2.awk"
wikidata="$2wikidata_undirected"
pythonscripts="$3"
overlapgraphscript="$pythonscripts""overlapgraph.py"

criterion=30

threshold=2
poolsize=16

#echo $wikidata
#echo $humanwhoscript
#echo $criterion

removetrivial='BEGIN{FS=";"}{if($2!=5&&$2!=6581097&&$2!=6581072&&$2!='$criterion')print$0}'
awk -v c=$criterion -f $humanwhoscript $wikidata | awk $removetrivial > criteriongraph.csv
python -u $overlapgraphscript -w -t $threshold -p $poolsize criteriongraph.csv | 
grep ";" | sort -V  

