# Analyzing-WikiData

This repository hosts various scripts for compression and analyzing WikiData.
Currently all scripts are AWK.Scripts. The output location must be added manually for the moment.

To execute it type
```sh
$ awk -f program-file input-file
```

## Explanations

**--compressing.awk**

The main compressing script uses the full (unzipped) turtle dump file as found on:
https://dumps.wikimedia.org/wikidatawiki/entities/   (i.e. latest-all.ttl)

| Input |
wds:Q457-9EEE3BB9-E8C4-495F-A4F8-9C338DABE5F8 a wikibase:Statement,
                wikibase:BestRank ;
        wikibase:rank wikibase:NormalRank ;
        ps:P1376 wd:Q1726747 ;
        prov:wasDerivedFrom wdref:cb1bf156a6906c27e02d4e4e7585aabcddd0e094 .

| Output |
wd:Q457 ps:P1376 wd:Q1726747


**--cutprefixes.awk**

This script cuts the prefixes and only leaves the actual numeric values for entites and properties.
As input file, the output of the first compressing script is used.
THe information wheather a property was a direct statement or a qualifier is lost at this stage.

| Input |
wd:Q457 ps:P1376 wd:Q1726747

| Output |
457 1376 1726747


--------------------------------------
> Further explanation of the other files will be provided soon...
