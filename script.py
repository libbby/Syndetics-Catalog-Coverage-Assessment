# This script will download XML files using the TRLN Endeca web services API and then parse them for data 'match-points' to search for Syndetics matches.
# Results are written to a CSV file in the same directory script lives in
# Libby Wilcher (https://github.com/libbby/Syndetics-Catalog-Coverage-Assessment), UNC Chapel Hill
# Script written and tested in Python 2.7
# Last updated: 22 October 2015

import webbrowser 
import lxml.etree as ET
import lxml.html as HTML
import urllib
import csv
import pdb
import time


def populateISBN():	# creates a list of Syndetics ISBNs for each item.
	global i
	global isbnx
	isbnx = []
	contains_isbn = child[1][0][i][1].find('Syndetics-ISBN')
	if contains_isbn != None:	# in case there are no ISBNs provided in the XML
		for node in child[1][0][i][1].find('Syndetics-ISBN').iter("item"):
			isbnx.append(node.text)	# update the list of ISBNs for that single item
	else:
		isbnx.append("unavailable")
	

def isbn1SyndTest(): # use this function on each ITEM in the Endeca XML to search for Syndetics info using the first Syndetics ISBN listed.
	global bool_isbn1_summary
	global bool_isbn1_toc
	global bool_isbn1_dbc
	global bool_isbn1_lc
	global bool_isbn1_mc
	global bool_isbn1_sc
	syn_doch_isbn1 = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbnx[0] + "/XML.XML&client=ncchapelh")) # for missing Syndetics results, parse them as HTML
	if syn_doch_isbn1.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
		bool_isbn1_summary = 0
		bool_isbn1_toc = 0
		bool_isbn1_dbc = 0
		bool_isbn1_lc = 0
		bool_isbn1_mc = 0
		bool_isbn1_sc = 0
	else:
		syn_docx_isbn1 = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbnx[0] + "/XML.XML&client=ncchapelh")) # parse the Syndetics results as XML, because there were not HTML tags present.
		if syn_docx_isbn1.find('SUMMARY') != None: # Searches Syndetics XML for a 'SUMMARY' tag
			bool_isbn1_summary = 1
		else:
			bool_isbn1_summary = 0 
		if syn_docx_isbn1.find('TOC') != None: # Same as above, but for 'TOC' tag
			bool_isbn1_toc = 1
		else:
			bool_isbn1_toc = 0
		if syn_docx_isbn1.find('DBCHAPTER') != None: # Same as above, but for 'DBCHAPTER' tag
			bool_isbn1_dbc = 1
		else:
			bool_isbn1_dbc = 0
		if syn_docx_isbn1.find('LC') != None: # Same as above, but for 'LC' tag
			bool_isbn1_lc = 1
		else:
			bool_isbn1_lc = 0
		if syn_docx_isbn1.find('MC') != None: # Same as above, but for 'MC' tag
			bool_isbn1_mc = 1
		else:
			bool_isbn1_mc = 0
		if syn_docx_isbn1.find('SC') != None: # Same as above, but for 'SC' tag
			bool_isbn1_sc = 1
		else:
			bool_isbn1_sc = 0
			
def isbn2xSynTest():
	global bool_isbn2x_summary
	global bool_isbn2x_toc
	global bool_isbn2x_dbc
	global bool_isbn2x_lc
	global bool_isbn2x_mc
	global bool_isbn2x_sc
	global syn_docx_isbn2x
	total_bool_isbn2x_summary = 0
	total_bool_isbn2x_toc = 0
	total_bool_isbn2x_dbc = 0
	total_bool_isbn2x_lc = 0
	total_bool_isbn2x_mc = 0
	total_bool_isbn2x_sc = 0
	y = 0
	z = int(child[1][0][i][1].xpath("count(./Syndetics-ISBN/item)"))	# the number of ISBNs associated with the particular item
	if z > 1:	
		for y in range(z):	# loops through each ISBN
			if y > 0:	# y = 0 is our ISBN1, we already did that one
				syn_doch_isbn2x = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbnx[y] + "/XML.XML&client=ncchapelh"))	# for missing Syndetics results, parse them as HTML
				if syn_doch_isbn2x.find('head') != None:	# passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
					bool_isbn2x_summary = 0
					bool_isbn2x_toc = 0 
					bool_isbn2x_dbc = 0
					bool_isbn2x_lc = 0
					bool_isbn2x_mc = 0
					bool_isbn2x_sc = 0
				else:	# starting the booleans at 0, not because they WILL be empty, but because we will be summing.
					bool_isbn2x_summary = 0
					bool_isbn2x_toc = 0 
					bool_isbn2x_dbc = 0
					bool_isbn2x_lc = 0
					bool_isbn2x_mc = 0
					bool_isbn2x_sc = 0
					syn_docx_isbn2x = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbnx[y] + "/XML.XML&client=ncchapelh"))
					if syn_docx_isbn2x.find('SUMMARY') != None: # Searches Syndetics XML for a 'SUMMARY' tag
						bool_isbn2x_summary = 1
					else:
						bool_isbn2x_summary = 0 
					if syn_docx_isbn2x.find('TOC') != None: # Same as above, but for 'TOC' tag
						bool_isbn2x_toc = 1
					else:
						bool_isbn2x_toc = 0
					if syn_docx_isbn2x.find('DBCHAPTER') != None: # Same as above, but for 'DBCHAPTER' tag
						bool_isbn2x_dbc = 1
					else:
						bool_isbn2x_dbc = 0
					if syn_docx_isbn2x.find('LC') != None: # Same as above, but for 'LC' tag
						bool_isbn2x_lc = 1
					else:
						bool_isbn2x_lc = 0
					if syn_docx_isbn2x.find('MC') != None: # Same as above, but for 'MC' tag
						bool_isbn2x_mc = 1
					else:
						bool_isbn2x_mc = 0
					if syn_docx_isbn2x.find('SC') != None: # Same as above, but for 'SC' tag
						bool_isbn2x_sc = 1
					else:
						bool_isbn2x_sc = 0
				total_bool_isbn2x_summary += bool_isbn2x_summary	# a running sum of whether any ISBN was associated with data type.
				total_bool_isbn2x_toc += bool_isbn2x_toc			# 0 means none were, 1 or more means at least one was.
				total_bool_isbn2x_dbc += bool_isbn2x_dbc
				total_bool_isbn2x_lc += bool_isbn2x_lc
				total_bool_isbn2x_mc += bool_isbn2x_mc
				total_bool_isbn2x_sc += bool_isbn2x_sc
			y += 1
			time.sleep(0.001)
		if total_bool_isbn2x_summary > 0:	# turn those total_ variables into booleans for our CSV
			bool_isbn2x_summary = 1
		if total_bool_isbn2x_toc > 0:
			bool_isbn2x_toc = 1
		if total_bool_isbn2x_dbc > 0:
			bool_isbn2x_dbc = 1
		if total_bool_isbn2x_lc > 0:
			bool_isbn2x_lc = 1
		if total_bool_isbn2x_mc > 0:
			bool_isbn2x_mc = 1
		if total_bool_isbn2x_sc > 0:
			bool_isbn2x_sc = 1
	else:	
		bool_isbn2x_summary = 0
		bool_isbn2x_toc = 0 
		bool_isbn2x_dbc = 0
		bool_isbn2x_lc = 0
		bool_isbn2x_mc = 0
		bool_isbn2x_sc = 0

def oclcSynTest(): # use this function on each ITEM in the Endeca XML to search for Syndetics info using the OCLC number listed.
	global bool_oclc_summary
	global bool_oclc_toc
	global bool_oclc_dbc
	global bool_oclc_lc
	global bool_oclc_mc
	global bool_oclc_sc
	if int(child[1][0][i][1].xpath("count(./OCLCNumber/item)")) == 0:
		bool_oclc_summary = 0
		bool_oclc_toc = 0
		bool_oclc_dbc = 0
		bool_oclc_lc = 0
		bool_oclc_mc = 0
		bool_oclc_sc = 0
	else:
		syn_doch_oclc = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(child[1][0][i][1].find('OCLCNumber/item').text))) # for missing Syndetics results, parse them as HTML
		if syn_doch_oclc.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
			bool_oclc_summary = 0
			bool_oclc_toc = 0
			bool_oclc_dbc = 0
			bool_oclc_lc = 0
			bool_oclc_mc = 0
			bool_oclc_sc = 0
		else:
			syn_docx_oclc = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(child[1][0][i][1].find('OCLCNumber/item').text)))
			if syn_docx_oclc.find('SUMMARY') != None: # Searches Syndetics XML for a 'SUMMARY' tag
				bool_oclc_summary = 1
			else:
				bool_oclc_summary = 0 
			if syn_docx_oclc.find('TOC') != None: # Same as above, but for 'TOC' tag
				bool_oclc_toc = 1
			else:
				bool_oclc_toc = 0
			if syn_docx_oclc.find('DBCHAPTER') != None: # Same as above, but for 'DBCHAPTER' tag
				bool_oclc_dbc = 1
			else:
				bool_oclc_dbc = 0
			if syn_docx_oclc.find('LC') != None: # Same as above, but for 'LC' tag
				bool_oclc_lc = 1
			else:
				bool_oclc_lc = 0
			if syn_docx_oclc.find('MC') != None: # Same as above, but for 'MC' tag
				bool_oclc_mc = 1
			else:
				bool_oclc_mc = 0
			if syn_docx_oclc.find('SC') != None: # Same as above, but for 'SC' tag
				bool_oclc_sc = 1
			else:
				bool_oclc_sc = 0
		#urllib.urlretrieve("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(child[1][0][i][1].find('OCLCNumber/item').text), child[1][0][i][0].text + ".xml")

def loopThrough():
	global i
	i = 0
	for node in child[1][0]:
		child.iter()
		isbn_count = int(child[1][0][i][1].xpath("count(./Syndetics-ISBN/item)"))
		otherauthor_count = int(child[1][0][i][1].xpath("count(./Other-Authors/item)"))
		#for i in range(n):	# this cycles through the ITEM tags that contain records data
		ice_toc = child[1][0][i][1].find('ICE-Chapter-Title')
		if ice_toc != None:	# if the tag ICE-Chapter-Title is not absent (that is, it IS present) Bool =1
			bool_ice_toc = 1
		else:	# if the tag is absent, Bool =0
			bool_ice_toc = 0
			
		main_author = child[1][0][i][1].find('Main-Author')
		if main_author != None:
			bool_main_author = 1
		else:
			bool_main_author = 0
			
		oclc_number = child[1][0][i][1].find('OCLCNumber')
		if oclc_number != None:
			bool_oclc = 1
		else:
			bool_oclc = 0
				
		upc = child[1][0][i][1].find('UPC')
		if upc != None:
			bool_upc = 1
		else:
			bool_upc = 0
		
		populateISBN()
		isbn1SyndTest()
		time.sleep(0.001)
		oclcSynTest()
		time.sleep(0.001)
		isbn2xSynTest()
			
		print child[1][0][i][0].text + ", " + str(bool_ice_toc) + ", " + str(bool_main_author) + ", " + str(bool_oclc) + ", " + str(bool_upc) + ", " + str(otherauthor_count) + ", " + str(isbn_count) + ", " + str(isbnx[0]) + ", " + str(bool_isbn1_summary) + ", " + str(bool_isbn1_toc) + ", " + str(bool_isbn1_dbc) + ", " + str(bool_isbn1_lc) + ", " + str(bool_isbn1_mc) + ", " + str(bool_isbn1_sc) + ", " + str(bool_oclc_summary) + ", " + str(bool_oclc_toc) + ", " + str(bool_oclc_dbc) + ", " + str(bool_oclc_lc) + ", " + str(bool_oclc_mc) + ", " + str(bool_oclc_sc) + ", " + str(bool_isbn2x_summary) + ", " + str(bool_isbn2x_toc) + ", " + str(bool_isbn2x_dbc) + ", " + str(bool_isbn2x_lc) + ", " + str(bool_isbn2x_mc) + ", " + str(bool_isbn2x_sc)
		c.writerow([collection_short, child[1][0][i][0].text, collection_short + child[1][0][i][0].text, bool_ice_toc, bool_main_author, bool_oclc, bool_upc, otherauthor_count, isbn_count, str(bool_isbn1_summary), str(bool_isbn1_toc), str(bool_isbn1_dbc), str(bool_isbn1_lc), str(bool_isbn1_mc), str(bool_isbn1_sc), str(bool_oclc_summary), str(bool_oclc_toc), str(bool_oclc_dbc), str(bool_oclc_lc), str(bool_oclc_mc), str(bool_oclc_sc), str(bool_isbn2x_summary), str(bool_isbn2x_toc), str(bool_isbn2x_dbc), str(bool_isbn2x_lc), str(bool_isbn2x_mc), str(bool_isbn2x_sc)])
		
		i += 1
			
MARC773 = raw_input("enter MARC773 field: ")	# Unique collection title string
MARC773 = MARC773.replace(" ", "_")
collection_short = raw_input("enter a 'shorthand' code for the collection: ")	# this is used to create a primary key for our database later.

endeca_url = "http://search.lib.unc.edu/search?Ntt=" + MARC773 + "&Ntk=Keyword&Nty=1&output-format=xml&facet-options=exclude-refinements&include-record-property=ICE+Chapter+Title&include-record-property=Syndetics+ISBN&include-record-property=OCLCNumber&include-record-property=UPC&include-record-property=Main+Author&include-record-property=Other+Authors&maximum-number-records=1000"
webbrowser.open(endeca_url)	# here's your XML file in browser, if you want it.
urllib.urlretrieve(endeca_url, MARC773 + ".xml")	# saves that XML into the same folder this script is in, the name is the MARC773 field you input earlier
c = csv.writer(open(MARC773 + ".csv", "wb"))
c.writerow(["Collection", "UNCb Identifier", "PK", "ICE ToC", "Main Author", "OCLC Number", "UPC", "Other Authors", "Syndetics ISBNs", "ISBN1:SUMMARY", "ISBN1:TOC", "ISBN1:DBCHAPTER", "ISBN1:LC", "ISBN1:MC", "ISBN1:SC", "OCLC:SUMMARY", "OCLC:TOC", "OCLC:DBCHAPTER", "OCLC:LC", "OCLC:MC", "OCLC:SC", "ISBN2X:SUMMARY", "ISBN2X:TOC", "ISBN2X:DBCHAPTER", "ISBN2X:LC", "ISBN2x:MC", "ISBN2X:SC"])

tree = ET.parse(MARC773 + ".xml")	# set up XML tree to parse
root = tree.getroot()

for child in root:	# tells us (and script) what child is
	root.iter()
	
number_ebooks = 0	# produces a count of ebooks in the given collection
for node in child[1][0]:
	number_ebooks += 1
print ("There are " + str(number_ebooks) + " ebooks in this collection.")

loopThrough()
