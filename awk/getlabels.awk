BEGIN{duplicate = ""}

#First searches for the beginning of a new entity and saves its number as "entity"
/wd:(Q|q).* a wikibase:Item/ {
	entity = $1; 
	sub(/wd:(Q|q)/,"",entity)
} 

#Searchs for lines containing a label definition and saves the found string as "label"
match($0, /rdfs:label \".*\"@../){
	label = substr($0, RSTART, RLENGTH);
	sub(/rdfs:label \"/,"",label);
	
#Combines the current entity number with its label and prints it when it has not been printed previously
	combined = entity" "label;
	if(combined != duplicate){
		print combined;
		duplicate = combined
	}
}
