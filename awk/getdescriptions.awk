BEGIN{duplicate = ""}

#First searches for the beginning of a new entity and saves its number as "entity"
/wd:(Q|q).* a wikibase:Item/ {
	entity = $1; 
	sub(/wd:(Q|q)/,"",entity)
} 

#Searchs for lines containing a description definition and saves the found string as "description"
match($0, /schema:description \".*\"@en/){
	description = substr($0, RSTART, RLENGTH);
	sub(/schema:description \"/,"",description);
	sub(/\"/,"",description);

#Combines the current entity number with its description and prints it when it has not been printed previously
	combined = entity" "description;
	if(combined != duplicate){
		print combined;
		duplicate = combined
	}
}
