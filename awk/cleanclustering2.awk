/[0-9]/{sub("Partition ","",$0);
sub(": Size: ",";",$0);
sub(" Members: \\[",";",$0);
sub("Partition ","",$0);
gsub("'","",$0);
gsub(", ",";",$0);
sub("\\]","",$0);
print $0}