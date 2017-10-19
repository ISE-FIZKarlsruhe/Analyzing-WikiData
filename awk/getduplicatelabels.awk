BEGIN {d=0;
prev = 0}

{if ($1 == d) {
  if(ppno != pno)
    print prev;
  print $0}
prevprev = prev;
ppno = prevprev;
sub(/ */,"",ppno);
prev = $0;
pno = $1;
d = $1
}