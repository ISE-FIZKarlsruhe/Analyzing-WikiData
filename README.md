# Analyzing-WikiData

This repository hosts various scripts for compression and analyzing WikiData.
Currently scripts are .awk-scripts an .py scripts.
The output location must sometimes be added manually.

Files that were created with the provided scripts can be found on:
https://drive.google.com/drive/folders/0B1VsD7AFoAMVb01BaGhMWXpscVU 
The folder "statistics" contains some preliminary analysis results.


## General Explanations

### Compress WikiData

1. Get the "latest-all.ttl" file from https://dumps.wikimedia.org/wikidatawiki/entities/ and unzip (bzip2 -d filename.bz2)
2. Run "compressing.awk"
3. Run "cutprefixes.awk"
4. Run "awk '{print $1";",$3}' inputfile" > outputfilename.csv"   

(The last commands removes the predicates from the "wikidata_numbers-only"-file. To retrieve the predicates for a given path, follow the instructions on insertpredicatestopath.awk)  

### Find all "Supertypes"
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

Alternatively use pandas with .csv (not tested)
 ```python
 import pandas as pd
 df = pd.read_csv(inputfile.csv, sep=";",names = ["0","1"])
	df = df.loc[~df['1'].isin(df['0'])]
	print(df.to_string(index=False, index_names=False))
```

4. Run getlabelsforentities.awk as decribed below


## python-script Explanations

Some scripts can be called directly from console via
 ```sh
$ python -u scriptname.py -h
```
(-u = unbuffered python output
-h = help, specifies the options)

###**--johnson2.py** [callable] 

Combines remZeroDeg.py and johnson.py to fine elementary circuits from the supertypegraph.csv file

-Output-
1678301
1678301
--
28128195
2537428
28128195
--
378681
26695607
378681
--



###**--remZeroDeg.py** [callable] [deprecated]

This script iteratively removes all nodes that have either InDegree=0 or Outdegree=0. Until every node has at least InDegree+Outdegree>1.

Input and Output is a two column .csv file. (For now used for the supertypesgraph to further process it with johnson.py)


Can be called directly from console via
 ```sh
$ python -u remZeroDeg.py [inputfile]
```
(-u = unbuffered python output)


###**--johnson.py** [callable] [deprecated]

A fast implementation to find simple circuits. Only works with files that do not contain 0-degree nodes. Therefore run "remZeroDeg.py" first. 
Found on https://gist.github.com/qpwo/44b48595c2946bb8f823e2d72f687cd8 

Input is a two column .csv file 
Output is a n-column dataframe containing a full elementary circle in each line. 

-Output-   
130050; 623365; 130050
130050; 623377; 130050
56658; 623365; 56658


###**--pathfinding.py**

This script has various pathfinding capabilities. 
Details regarding its parameters can be found in comments next to the code itself.  

The scrips uses a further reduced "numbers-only"-file, that only contains the entity and its objects (no predicates).
The input file is created as follows:

The Script privides multiple options that are explained with comments within the code.  

In the current version it requires approximately 8GB of free RAM and robustly finds all shortest paths from a given entity to all other entities for an unlimited (testing in progress) pathlength.   



## AWK-script Explanations

To execute a awk script type
```sh
$ awk -f program-file inputfile1 [inputfile2]
```

###**--compressing.awk**

The main compressing script uses the full (unzipped) turtle dump file as found on:
https://dumps.wikimedia.org/wikidatawiki/entities/   (i.e. latest-all.ttl)  

-Input-  
wds:Q457-9EEE3BB9-E8C4-495F-A4F8-9C338DABE5F8 a  wikibase:Statement,  
wikibase:BestRank ;  
wikibase:rank wikibase:NormalRank ;  
ps:P1376 wd:Q1726747 ;  
prov:wasDerivedFrom wdref:cb1bf156a6906c24e4e7585aabcddd0e094 .  

-Output-   
wd:Q457 ps:P1376 wd:Q1726747  

###**--compressing_wdt.awk** 

Works similar to the previous script but only considers statement of rdf:type wikibase:BestRank.
It therefore also ignores qualifiers.  

###**--cutprefixes.awk** 

This script cuts the prefixes and only leaves the actual numeric values for entites and properties.
As input file, the output of the first compressing script is used.
THe information wheather a property was a direct statement or a qualifier is lost at this stage.

-Input- 
wd:Q457 ps:P1376 wd:Q1726747 
or 
wd:Q457 wdt:P1376 wd:Q1726747   

-Output- 
457 1376 1726747  


###**--rdftype-subclass_graph.awk** 

Retireves a graph of all edges the go through either P31 (RDF:Type) or P297 (subClassOf)

Input is the compressed wikidata file containing the predicates and prefixes.

-Output- 
1 41719
1 26961029
1 36906466
2 3504248
3 937228

###**--getobjects.awk** 

Asks the User for the number of a specific entity and prints all of its predicates and objects. 
It is intendet to be used on the maximally compressed wikidata file (the one containing only numbers).  

###**--getlabels.awk** 

This Script uses the unzipped main file [latest-all.ttl] to extract all available labels for every entity.
In oder to only get the english labels use on the first output

```sh
$ grep "@en" input-file
```

Note that the output includes many duplicates and name variations for the same entity. 
The file labels_english has been stripped down to the maximum. 

Name variations within the english labels of an entity can be found with the getduplicatelabels.awk script.  

###**--getobjectcount.awk, getobjectcount2.awk** 
!Deprecated. Better visualized by the degreeplot!

These have been used to get some idea about the number of objects an entity links to. 
The first script counts the links each individual entity has.
The second script uses the results of the first one to aggregate the results in a way showing how many entities there are for a given number of links.

###**--getlabelsforlist.awk**

Adds the labels to a list of entities. The list does not have to ordered.

```sh
$ awk -f getlabelsforlist.awk labelfile numberlist 
```

-Example labelfile-  
2	Label for entity 2
78 	Anderes Label
...  

-Example numberlist-  
38
145
78
...

###**--getlabelforpath.awk** [better use getlabelforlist.awk]  

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

To get a proper output, it needs to be sorted afterwards. To do it in one step type the following:

```sh
$ awk -f insertprefixestopath.awk inputfile1 inputfile2 | sort -V
```

-Example output-  
Step 0: Q78 Basel  
Step 1: Q39 Switzerland
Step 2: Q183 Germany
Step 3: Q567 Angela Merkel

###**--getlabelsforentities.awk** 

The script takes a list of entities inputfile1, and the wikidata label file form getlabels.awk as iputfile2. 

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
```sh
$ awk -f getlabelsforentities.awk inputfile1 inputfile2
```

###**--insertpredicatestopath.awk** 

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

To get a proper output, it needs to be sorted afterwards. To do it in one step type the following:

```sh
$ awk -f insertpredicatestopath.awk inputfile1 inputfile2 | sort -V
```

-Example output-  
Step 0: wd:Q78 ps:P17 wd:Q39  
Step 1: wd:Q39 ps:P47 wd:Q183  
Step 1: wd:Q39 ps:P530 wd:Q183  
Step 2: wd:Q183 ps:P6 wd:Q567  
Step 3: wd:Q567 pq:P812 wd:Q413  



---
_Informations and further explanations will be updated accordingly._
