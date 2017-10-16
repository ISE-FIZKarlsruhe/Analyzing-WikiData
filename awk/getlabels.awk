BEGIN{duplicate = ""}
/wd:(Q|q).* a wikibase:Item/ {
	entity = $1; 
	sub(/wd:(Q|q)/,"",entity)
} 
match($0, /rdfs:label \".*\"@../){
	label = substr($0, RSTART, RLENGTH);
	sub(/rdfs:label \"/,"",label);
	

	combined = entity" "label;
	if(combined != duplicate){
		print combined;
		duplicate = combined
	}
		
}
