BEGIN{d = " "}
{if ($1 !~ d) {
printf "\n%s; ", $1;
d = $1}
printf "%s; ", $3}