{sub(/wd:Q/,"",$1);
sub(/ps:P/,"",$0);
sub(/pq:P/,"",$0);
sub(/wd:Q/,"",$3);
sub(/wdt:P/,"",$0);
print $0}