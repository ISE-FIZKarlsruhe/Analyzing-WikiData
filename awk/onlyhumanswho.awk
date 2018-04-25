BEGIN{d = 0; crit = 0}
{if($1+0 != d){
	if(crit == 1) print d;
	crit = 0}
if($2+0 == 183+0)crit = 1;
d = $1
}