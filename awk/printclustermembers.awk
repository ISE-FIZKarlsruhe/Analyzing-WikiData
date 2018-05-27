match($0, /\[(.*)\]/, a) {
o = a[1]; 
sub("\\[","",o);
sub("\\]","",o);
gsub("'","",o);
gsub(", ","\n",o);
print o}