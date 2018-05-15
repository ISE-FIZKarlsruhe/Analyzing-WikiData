input="$1"
snaplocation="$2"
#grep “;” overlapgraph | sort –V > overlapgraph_clean
awk 'BEGIN{FS=";"}/^[0-9;\.]+$/{print $1,$2}' overlapgraph > overlapgraph_forsnap.txt
python ../../py/snap_environment/snap_test.py overlapgraph_forsnap.txt > maxwcc
grep "^[0-9]\+" maxwcc | sed 's/\r//' > maxwcc_members
join -t";" overlapgraph maxwcc_members