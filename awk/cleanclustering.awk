match($0, /'(.*)'/, a) {
o = a[1]; 
sub(" Members: \\[",";",o);
gsub("'","",o);
gsub(", ",";",o);
print o}