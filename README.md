# Analyzing-WikiData

This repository hosts various scripts for compression and analyzing WikiData.
Currently all scripts are .awk-scripts. The output location must be added manually for the moment.

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
4. Run "awk '{print $1";",$3}' inputfile" > outputfilename.csv"   

(The last commands removes the predicates from the "wikidata_numbers-only"-file, as they are not processed by the python script. To retrieve the predicates for a given path, follow the instructions on insertpredicatestopath.awk)  

The Script privides multiple options that are explained with comments within the code.  

In the current version it requires approximately 8GB of free RAM and robustly finds all shortest paths from a given entity to all other entities for an unlimited (testing in progress) pathlength.   

### General Explanations

####**--Find all "Supertypes"**
1. Input is the prefixed WikiData file:
wd:Q457 ps:P1376 wd:Q1726747

2. Run rdftype-subclass_graph.awk to retireve a graph of all edges the go through either P31 (RDF:Type) or P297 (subClassOf) 

3. Use the graph .txt file from the previous step with python snap. This gets all Entities with OutDegree of 0.

 ```python
 import snap
 G1 = snap.LoadEdgeList(snap.PNGraph, "inputfile.txt", 0, 1)
 for NI in G1.Nodes():
 	if NI.GetOutDeg() == 0:
 		print NI.GetId()
```

3. Run getlabelsforentities as decribed below

### AWK-script Explanations

To execute a awk script type
```sh
$ awk -f program-file input-file
```

#####**--compressing.awk**

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

#####**--compressing_wdt.awk** 

Works similar to the previous script but only considers statement of rdf:type wikibase:BestRank.
It also ignores qualifiers.  

#####**--cutprefixes.awk** 

This script cuts the prefixes and only leaves the actual numeric values for entites and properties.
As input file, the output of the first compressing script is used.
THe information wheather a property was a direct statement or a qualifier is lost at this stage.

-Input- 
wd:Q457 ps:P1376 wd:Q1726747 
or 
wd:Q457 wdt:P1376 wd:Q1726747   

-Output- 
457 1376 1726747  

#####**--getobjects.awk** 

This script asks the User for the number of a specific entity and prints all of its predicates and objects. 
It is intendet to be used on the maximally compressed wikidata file (the one containing only numbers).  

#####**--getlabels.awk** 

This Script uses the unzipped main file [latest-all.ttl] to extract all available labels for every entity.
In oder to only get the english labels use

```sh
$ grep "@en" input-file
```

Note that the output includes many duplicates and name variations for the same entity. 
The file labels_english has been stripped down to the maximum. 

Name variations within the english labels of an entity can be found with the getduplicatelabels.awk script.  

#####**--getobjectcount.awk, getobjectcount2.awk** 

These have been used to get some idea about the number of objects an entity links to. 
The first script counts the links each individual entity has.
The second script uses the results of the first one to aggregate the results in a way showing how many entities there are for a given number of links.

I.e. the lines

>1 7944479  
>2 8342598  
>3 5060407  

indicate that there are 7944479 entities which are connected to exactly one other entity, 8342598 entities that link to exactly 2 other entities and so on.  

#####**--getlabelforpath.awk** 

The script takes a path between two entites as generated as output from the python pathfinding script as inputfile1, and the wikidata label file as iputfile2. The output will be the path (without predicates) with labels for each entity.

-Example inputfile1-  
78 39  
39 183  
183 567  
567 413  

-Example inputfile2-  
1 Universe  
2 Earth  
3 Life  
4 Death  
...  

To properly execute the script, the output needs to be sorted afterwards. To do it in one step type the following:

```sh
$ awk -f insertprefixestopath.awk inputfile1 inputfile2 | sort -V
```


-Example output-  
Step 0: Q78 Basel  
Step 1: Q39 Switzerland
Step 2: Q183 Germany
Step 3: Q567 Angela Merkel

#####**--getlabelsforentities.awk** 

The script takes a list of entities inputfile1, and the wikidata label file as iputfile2.

-Example inputfile1-  
1  
2  
3  
4  
...  

-Example inputfile2-  
1 Universe  
2 Earth  
3 Life  
4 Death  
...  

To properly execute the script, all files must be sorted. 


#####**--insertpredicatestopath.awk** 

The script takes a path between two entites as generated as output from the python pathfinding script as inputfile1, and the compressed wikidata including prefixes as iputfile2. The output will be the full path containing also the possible predicates for each step.

-Example inputfile1-  
78 39  
39 183  
183 567  
567 413  

-Example inputfile2-  
wd:Q1 ps:P2959 wd:Q22924128  
wd:Q2 pq:P17 wd:Q736  
wd:Q2 pq:P17 wd:Q837  
wd:Q2 pq:P248 wd:Q23859820  
wd:Q2 pq:P248 wd:Q24206672  
...  

To properly execute the script, the output needs to be sorted afterwards. To do it in one step type the following:

```sh
$ awk -f insertprefixestopath.awk inputfile1 inputfile2 | sort -V
```

-Example output-  
Step 0: wd:Q78 ps:P17 wd:Q39  
Step 1: wd:Q39 ps:P47 wd:Q183  
Step 1: wd:Q39 ps:P530 wd:Q183  
Step 2: wd:Q183 ps:P6 wd:Q567  
Step 3: wd:Q567 pq:P812 wd:Q413  



---
_Informations and further explanations will be updated accordingly._
