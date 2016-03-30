# E-collections discovery evaluation: catalog data
This suite of scripts is used to gather data on the discoverability (in our main online catalog) of individual titles within collections. The output of the scripts is at the individual title (i.e. bibliographic record) level. The script output is ingested into a database used to compile collection-level reports. 

## Questions this is intended to answer for each collection: 
* How many titles are represented by MARC records are in the catalog?
  * This number is to be compared with the number of titles the content provider says we should have
  * We cannot assume/expect exactly matching numbers here due to the existence of multi-volume (or multi-"CD", etc.) e-items and inconsistency in how these are represented, both in MARC records and provider title lists.
* Given the current catalog user interface configuration, how many titles display supplemental content from SyndeticsSolutions at load time: book cover image, table of contents, summary, first chapter, etc.? 
  * How much does this number increase if we change the catalog user interface configuration to send additional match points for each title? 
* How many titles have *indexed, searchable* table of contents data from Syndetics (ICE data) available in the catalog? 
* How many titles have standard classification numbers assigned? LCSH and MeSH are counted.
* What is the richness of the author and standardized subject access points in the records?

# Usage
## Overview of steps
1. Prepare collection list -- this is a tab-delimited text file, with one collection per line.
2. Run the first script with the collection list as input. This produces a list of unsuppressed (i.e. viewable in the public catalog) bib records on which to gather data.
3. Run the second script on the bib record list. This gets some pieces of data that can only be grabbed from the ILS versions of the records. 
4. Run the third script on the bib/ILS data list. This pulls in the data that can only be grabbed by examining the live public catalog records, or querying the Syndetics API. 
5. Import results of the third script into the database to compile collection-level stats/reports.

## Steps in detail
### Prepare collection list
* Format: tab-delimited text file
* File extension: .txt
* Line endings: Unix
* Data
  * Element 1: Collection name to search on in the catalog. See below for more details on this.
  * Element 2: A brief "shortcut" code for the collection. This is used instead of the full collection title string in the database to collapse the individual records into the correct collections, and to create a "this-record-in-this-collection" key, since some records will be part of more than one collection. 

#### More on collection name
* This will be the "Host Item" title (or part of it) that appears in the 773 field in bib records for e-resource collections that are processed by AAL/E-Resources Cataloging. These are the titles that include "(online collection)".
* The query built with the collection name as entered will be a left-anchored phrase match
* The type of query, combined with the structure/design of the assigned collection titles means that we can control the granularity of our reporting by how we enter the collection titles. Example: 
  * This would retrieve all the ACS Symposium Series titles: ACS symposium series (online collection)
  * This would retrieve just the ACS titles in the 2015 collection: ACS symposium series (online collection). 2015
  * This would retrieve all the ACS titles from 2011-2015 collections: ACS symposium series (online collection). 201 *(Note that this wouldn't include titles from the ACS 2010 collection because those were included in the same purchase as the backfile (1949-2009), and so they use the collection title: ACS symposium series (online collection). 1949-2010)*
  * UNC staff can look up the 773-field collection titles for all e-resource collections. Instructions on how to access and use this data are here: https://intranet.lib.unc.edu/wikis/staff/index.php/E-Resources_collection_data
