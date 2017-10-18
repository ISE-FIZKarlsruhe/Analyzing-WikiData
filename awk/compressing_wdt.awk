BEGIN {i = 0}
/^wds:/ {k = $0;
	sub(/-.*/,"",k);
 	sub(/s/,"",k);
 	sub(/q/,"Q",k)}
/BestRank/,/\./{command = "awk '/:.*ps.*wd:/ {if ($0 ~ /p.*,/) {q = $2} if ($2 ~ /wd:/) {$3 = $2; $2 = q} sub(/,/,\"\",$0); sub(/ps/,\"wdt\",$0); if ($0 != d) print $1,$2,$3 > (\"results/reduced5\"); d = $0}'"
print k,$0 | command }