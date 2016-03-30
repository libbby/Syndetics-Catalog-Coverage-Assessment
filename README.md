# E-collections discovery evaluation: catalog data
This suite of scripts is used to gather data on the discoverability (in our main online catalog) of individual titles within collections. The output of the scripts is at the individual title (i.e. bibliographic record) level. The script output is ingested into a database used to compile collection-level reports. 

## Questions this is intended to answer for each collection: 
* How many titles are represented by MARC records are in the catalog?
.* This number is to be compared with the number of titles the content provider says we should have
.* We cannot assume/expect exactly matching numbers here due to the existence of multi-volume (or multi-"CD", etc.) e-items and inconsistency in how these are represented, both in MARC records and provider title lists.
* Given the current catalog user interface configuration, how many titles display supplemental content from SyndeticsSolutions at load time: book cover image, table of contents, summary, first chapter, etc.? 
.* How much does this number increase if we change the catalog user interface configuration to send additional match points for each title? 
* How many titles have *indexed, searchable* table of contents data from Syndetics (ICE data) available in the catalog? 
* How many titles have standard classification numbers assigned? LCSH and MeSH are counted.
* What is the richness of the author and standardized subject access points in the records?

# Usage
## Overview of steps
1. Prepare collection list -- this is a tab-delimited text file, with one collection per line.
