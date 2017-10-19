BEGIN{
print "Number of subject?";
getline subject < "/dev/tty";
subject = "^"subject"$"}
{if ($1 ~ subject) print $2,$3}