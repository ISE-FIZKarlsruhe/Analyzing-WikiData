BEGIN{i= 0}

#building regex-array from file 1
NR==1{a[i]="^"$1+0"\\s.*$";i++}
FNR==NR{a[i]="^"$2+0"\\s.*$";i++;next} 

#for each line in file 2, check if line matches any regex from file1
{for (key in a){
	if ($0 ~ a[key]) {
		print "Step "key": Q"$0;
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
