BEGIN{max=0}

/: [0-9]/ {if ($2+0 > max)
	max = $2+0;
x = $2+0;
arr[x]++}

END {for (i=0; i <= max; i++)
	print i";",arr[i] > "statistics/pathcounts_Q1"}