BEGIN{p=0}
{if ($1 != p){a = 0; p=$1}
a++; 
if (a == 10) print $1}