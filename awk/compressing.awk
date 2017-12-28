BEGIN {i = 0
print ("compressing...")}
/^wds:/ {k = $0;
	sub(/-.*/,"",k);
 	sub(/s/,"",k);
 	sub(/q/,"Q",k)}
/^wds:[Qq].*-/,/\./ {command = "awk '/:.*wd:[Qq]/ {if ($0 !~ /item/) {if ($0 ~ /p.*,/) {q = $2} if ($2 ~ /wd:/) {$3 = $2; $2 = q} sub(/,/,\"\",$0); if ($0 != d) print $1,$2,$3 > (\"results/wikidata_compressed\"); d = $0}}'"
print k,$0 | command }
END {print "Done!"}
