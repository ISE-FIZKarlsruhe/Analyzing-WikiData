BEGIN{i= 0;j=0}

#building array from file 1
FNR==NR{a[i]=$1+0;i++;next} 
#e saves the total number of entities for which labels should be found
FNR==1{e=i}

#build regex
{regex = "^"a[j]"\\s.*$";
#if labelfile is more advanced than currently searched entity, search for the next entity
if ($1 > a[j]+0 && e>j){
	print a[j]" -- no label --";
	j++}
#check if entity is found and if so, print label
if ($0 ~ regex) {
	j++;
	print $0;
    }	
}