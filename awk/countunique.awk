BEGIN{FS=";"; d = 0; c= 0}
{if($1 != d){
	c++;
	d = $1
} 
}END {print c}