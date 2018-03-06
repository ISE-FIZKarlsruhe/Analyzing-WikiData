NR==FNR{a[$1+0]=$0;next}
{if(a[$0+0]!=""){print a[$0+0]}
else{print $0}}