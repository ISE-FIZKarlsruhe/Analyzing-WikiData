BEGIN{max=0}

{if ($1 > max)
	max = $1;
arr[$1]++}

END {for (i=1; i < max; i++)
	print i,arr[i] > "results/counts"}