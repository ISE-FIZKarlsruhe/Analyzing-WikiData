match($0, /'\''(.*)'\''/, a) {
o = a[1]; 
gsub("'\''","",o);
gsub(", ",";",o);
print o}