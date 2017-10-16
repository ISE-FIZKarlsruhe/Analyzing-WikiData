BEGIN{subject = "^5000420$"}
{if ($1 ~ subject) print $2,$3}