BEGIN{i= 0}

#building regex-array from file 1
FNR==NR{a[i]="^wd:Q"$1"\\s.*wd:Q"$2+0"$";i++;next} 

#for each line in file 2, check if line matches any regex from file1
{for (key in a){
	if ($0 ~ a[key]) {
		print "Step "key": "$0;
		viewd = $1;
		found = key
    	}	
	}
	if ($1 != viewd)
   	delete a[found]

   	#exit script when all regex have been found
   	if (length(a) == 0)
   		exit 1
} 

