# Analyzing-WikiData

This repository hosts various scripts for compression and analyzing WikiData.
Currently all scripts are .awk-scripts. The output location must be added manually for the moment.

To execute a script type
```sh
$ awk -f program-file input-file
```

Files that were created with the provided scripts can be found on:
https://drive.google.com/drive/folders/0B1VsD7AFoAMVb01BaGhMWXpscVU 

The folder "statistics" contains some preliminary analysis results.


### python-script Explanations

**--pathfinding.py**

This script has various pathfinding capabilities. 
Details regarding its parameters can be found in comments next to the code itself.  

The scrips uses a further reduced "numbers-only"-file, that only contains the entity and its objects (no predicates).
The input file is created as follows:
1. Get the "latest-all.ttl" file from https://dumps.wikimedia.org/wikidatawiki/entities/ and unzip
2. Run "compressing.awk"
3. Run "cutprefixes.awk"
4. Run "awk {print $1";",$3}' inputfile"


### AWK-script Explanations

**--compressing.awk**

The main compressing script uses the full (unzipped) turtle dump file as found on:
https://dumps.wikimedia.org/wikidatawiki/entities/   (i.e. latest-all.ttl)  

-Input-  
wds:Q457-9EEE3BB9-E8C4-495F-A4F8-9C338DABE5F8 a wikibase:Statement, 
wikibase:BestRank ; 
wikibase:rank wikibase:NormalRank ; 
ps:P1376 wd:Q1726747 ; 
prov:wasDerivedFrom wdref:cb1bf156a6906c27e02d4e4e7585aabcddd0e094 .  

-Output-   
wd:Q457 ps:P1376 wd:Q1726747  

**--compressing_wdt.awk** 

Works similar to the previous script but only considers statement of rdf:type wikibase:BestRank.
It also ignores qualifiers.  

**--cutprefixes.awk** 

This script cuts the prefixes and only leaves the actual numeric values for entites and properties.
As input file, the output of the first compressing script is used.
THe information wheather a property was a direct statement or a qualifier is lost at this stage.

-Input- 
wd:Q457 ps:P1376 wd:Q1726747 
or 
wd:Q457 wdt:P1376 wd:Q1726747   

-Output- 
457 1376 1726747  

**--getobjects.awk** 

This script asks the User for the number of a specific entity and prints all of its predicates and objects. 
It is intendet to be used on the maximally compressed wikidata file (the one containing only numbers).  

**--getlabels.awk** 

This Script uses the unzipped main file [latest-all.ttl] to extract all available labels for every entity.
In oder to only get the english labels use

```sh
$ grep "@en" input-file
```

Note that the output includes many duplicates and name variations for the same entity. 
The file labels_english has been stripped down to the maximum. 

Name variations within the english labels of an entity can be found with the getduplicatelabels.awk script.  

**--getobjectcount.awk, getobjectcount2.awk** 

These have been used to get some idea about the number of objects an entity links to. 
The first script counts the links each individual entity has.
The second script uses the results of the first one to aggregate the results in a way showing how many entities there are for a given number of links.

I.e. the lines

>1 7944479  
>2 8342598  
>3 5060407  

indicate that there are 7944479 entities which are connected to exactly one other entity, 8342598 entities that link to exactly 2 other entities and so on.  


---
_Informations and further explanations will be updated accordingly._
