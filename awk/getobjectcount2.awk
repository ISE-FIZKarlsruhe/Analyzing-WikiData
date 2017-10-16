BEGIN{max=0}

{if ($2 > max)
	max = $2;
arr[$2]++}

END {for (i=1; i < max; i++)
	if(arr[i] != "") print i,arr[i] > "results/absolutes"}