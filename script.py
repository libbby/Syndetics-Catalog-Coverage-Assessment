# This script will download XML files using the TRLN Endeca web services API and then parse them for data 'match-points' to search for Syndetics matches.
# Results are written to a CSV file in the same directory script lives in
# Libby Wilcher (https://github.com/libbby/Syndetics-Catalog-Coverage-Assessment), UNC Chapel Hill
# Script written and tested in Python 2.7
# Last updated: 03 February 2016

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
	contains_isbn = child[1][1][i][2].find('Syndetics-ISBN')
	if contains_isbn != None:	# in case there are no ISBNs provided in the XML
		for node in child[1][1][i][2].find('Syndetics-ISBN').iter("item"):
			isbnx.append(node.text)	# update the list of ISBNs for that single item
	else:
		isbnx.append("unavailable")
	
def isEbook(): # test for determing if item is an ebook
	global bool_is_ebook
	total_bool_is_ebook = 0
	f = 0
	for f in range(format_count):
		is_ebook = child[1][1][i][0][0][1][f][1].text
		if is_ebook == "eBook":
			bool_is_ebook = 1
		else:
			bool_is_ebook = 0
		total_bool_is_ebook += bool_is_ebook
		f += 1
	if total_bool_is_ebook > 0:
		bool_is_ebook = 1
	else:
		bool_is_ebook = 0
	
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
	z = int(child[1][1][i][2].xpath("count(./Syndetics-ISBN/item)"))	# the number of ISBNs associated with the particular item
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
	if bool_is_ebook == 0:
		if int(child[1][1][i][2].xpath("count(./OCLCNumber/item)")) == 0:
			bool_oclc_summary = 0
			bool_oclc_toc = 0
			bool_oclc_dbc = 0
			bool_oclc_lc = 0
			bool_oclc_mc = 0
			bool_oclc_sc = 0
		else:
			syn_doch_oclc = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(child[1][1][i][2].find('OCLCNumber/item').text))) # for missing Syndetics results, parse them as HTML
			if syn_doch_oclc.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
				bool_oclc_summary = 0
				bool_oclc_toc = 0
				bool_oclc_dbc = 0
				bool_oclc_lc = 0
				bool_oclc_mc = 0
				bool_oclc_sc = 0
			else:
				syn_docx_oclc = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(child[1][1][i][2].find('OCLCNumber/item').text)))
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
			#urllib.urlretrieve("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(child[1][1][i][2].find('OCLCNumber/item').text), child[1][1][i][0].text + ".xml")
			time.sleep(0.001)
	else:
		bool_oclc_summary = "null"
		bool_oclc_toc = "null" 
		bool_oclc_dbc = "null" 
		bool_oclc_lc = "null"
		bool_oclc_mc = "null"
		bool_oclc_sc = "null"
		
def upcSynTest(): # use this function on each ITEM in the Endeca XML to search for Syndetics info using the OCLC number listed.
	global bool_upc_avsummary
	global bool_upc_toc
	global bool_upc_dbc
	global bool_upc_lc
	global bool_upc_mc
	global bool_upc_sc
	if bool_is_ebook == 0:
		if int(child[1][1][i][2].xpath("count(./UPC/item)")) == 0:
			bool_upc_avsummary = 0
			bool_upc_toc = 0
			bool_upc_dbc = 0
			bool_upc_lc = 0
			bool_upc_mc = 0
			bool_upc_sc = 0
		else:
			syn_doch_upc = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=&upc=" + str(child[1][1][i][2].find('UPC/item').text))) # for missing Syndetics results, parse them as HTML
			if syn_doch_upc.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
				bool_upc_avsummary = 0
				bool_upc_toc = 0
				bool_upc_dbc = 0
				bool_upc_lc = 0
				bool_upc_mc = 0
				bool_upc_sc = 0
			else:
				syn_docx_upc = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=&upc=" + str(child[1][1][i][2].find('UPC/item').text)))
				if syn_docx_upc.find('AVSUMMARY') != None: # Searches Syndetics XML for an 'AVSUMMARY' tag
					bool_upc_avsummary = 1
				else:
					bool_upc_summary = 0 
				if syn_docx_upc.find('TOC') != None: # Same as above, but for 'TOC' tag
					bool_upc_toc = 1
				else:
					bool_upc_toc = 0
				if syn_docx_upc.find('DBCHAPTER') != None: # Same as above, but for 'DBCHAPTER' tag
					bool_upc_dbc = 1
				else:
					bool_upc_dbc = 0
				if syn_docx_upc.find('LC') != None: # Same as above, but for 'LC' tag
					bool_upc_lc = 1
				else:
					bool_upc_lc = 0
				if syn_docx_upc.find('MC') != None: # Same as above, but for 'MC' tag
					bool_upc_mc = 1
				else:
					bool_upc_mc = 0
				if syn_docx_upc.find('SC') != None: # Same as above, but for 'SC' tag
					bool_upc_sc = 1
				else:
					bool_upc_sc = 0
			#urllib.urlretrieve("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(child[1][1][i][2].find('UPC/item').text), child[1][1][i][2].text + ".xml")
			time.sleep(0.001)
	else:
		bool_upc_avsummary = "null"
		bool_upc_toc = "null" 
		bool_upc_dbc = "null" 
		bool_upc_lc = "null"
		bool_upc_mc = "null"
		bool_upc_sc = "null"	
		
def loopThroughInputList():
	global il
	il = 0
	global MARC773
	global child
	global collection_short
	
	while il < len(MARC773s):
		MARC773 = MARC773s[il]
		collection_short = raw_input("enter a 'shorthand' code for the collection "+MARC773+": ")	# this is used to create a primary key for our database later.
		MARC773 = MARC773.replace(" ", "_")
		#endeca_url = "http://search.lib.unc.edu/search?Nf=PubDateSort|BTWN%202014%202015&action=or:206605,false&Nty=1&output-format=xml&facet-options=exclude-refinements&include-record-property=ICE+Chapter+Title&include-record-property=Syndetics+ISBN&include-record-property=OCLCNumber&include-record-property=UPC&include-record-property=Primary+URL&include-record-property=Main+Author&include-record-property=Other+Authors&maximum-number-records=1000&record-options=include-record-facets&include-record-property=Format" #UPC TEST URL
		endeca_url = "http://search.lib.unc.edu/search?Ntt=" + MARC773 + "&Ntk=Keyword&Nty=1&output-format=xml&facet-options=exclude-refinements&include-record-property=ICE+Chapter+Title&include-record-property=Syndetics+ISBN&include-record-property=OCLCNumber&include-record-property=UPC&include-record-property=Main+Author&include-record-property=Other+Authors&include-record-property=Primary+URL&maximum-number-records=1000000&record-options=include-record-facets&include-record-property=Format" #REAL URL
		webbrowser.open(endeca_url)	# here's your XML file in browser, if you want it.
		urllib.urlretrieve(endeca_url, MARC773 + ".xml")	# saves that XML into the same folder this script is in, the name is the MARC773 field you input earlier
		
		tree = ET.parse(MARC773 + ".xml")	# set up XML tree to parse
		root = tree.getroot()
		for child in root:	# tells us (and script) what child is
			root.iter()
		
		number_ebooks = child[1][0][2].text	# produces a count of ebooks in the given collection
		print ("There are " + str(number_ebooks) + " ebooks in this title collection.")
				
		loopThroughXML()
		
		il += 1
		
def loopThroughXML():
	global i
	global format_count
	i = 0
	
	for node in child[1][1]:
		child.iter()
		isbn_count = int(child[1][1][i][2].xpath("count(./Syndetics-ISBN/item)"))
		otherauthor_count = int(child[1][1][i][2].xpath("count(./Other-Authors/item)"))
		primary_url_count = int(child[1][1][i][2].xpath("count(./Primary-URL/item)"))
		format_count = int(child[1][1][i][0][0].xpath("count(./dimensionValues/item)"))
		isEbook()
		
		ice_toc = child[1][1][i][2].find('ICE-Chapter-Title')
		if ice_toc != None:	# if the tag ICE-Chapter-Title is not absent (that is, it IS present) Bool =1
			bool_ice_toc = 1
		else:	# if the tag is absent, Bool =0
			bool_ice_toc = 0
			
		main_author = child[1][1][i][2].find('Main-Author')
		if main_author != None:
			bool_main_author = 1
		else:
			bool_main_author = 0
			
		oclc_number = child[1][1][i][2].find('OCLCNumber')
		if oclc_number != None:
			bool_oclc = 1
		else:
			bool_oclc = 0
				
		upc = child[1][1][i][2].find('UPC')
		if upc != None:
			bool_upc = 1
		else:
			bool_upc = 0
		
		populateISBN()
		isbn1SyndTest()
		time.sleep(0.001)
		oclcSynTest()
		upcSynTest()
		isbn2xSynTest()
			
		print child[1][1][i][1].text + ", " + str(bool_ice_toc) + ", " + str(bool_main_author) + ", " + str(bool_oclc) + ", " + str(bool_upc) + ", " + str(otherauthor_count) + ", " + str(isbn_count) + ", " + str(primary_url_count) + ", " + str(bool_is_ebook) + ", " + str(isbnx[0]) + ", " + str(bool_isbn1_summary) + ", " + str(bool_isbn1_toc) + ", " + str(bool_isbn1_dbc) + ", " + str(bool_isbn1_lc) + ", " + str(bool_isbn1_mc) + ", " + str(bool_isbn1_sc) + ", " + str(bool_oclc_summary) + ", " + str(bool_oclc_toc) + ", " + str(bool_oclc_dbc) + ", " + str(bool_oclc_lc) + ", " + str(bool_oclc_mc) + ", " + str(bool_oclc_sc) + ", " + str(bool_upc_avsummary) + ", " + str(bool_upc_toc) + ", " + str(bool_upc_dbc) + ", " + str(bool_upc_lc) + ", " + str(bool_upc_mc) + ", " + str(bool_upc_sc) + ", " + str(bool_isbn2x_summary) + ", " + str(bool_isbn2x_toc) + ", " + str(bool_isbn2x_dbc) + ", " + str(bool_isbn2x_lc) + ", " + str(bool_isbn2x_mc) + ", " + str(bool_isbn2x_sc)
		c.writerow([collection_short, child[1][1][i][1].text, collection_short + child[1][1][i][1].text, bool_ice_toc, bool_main_author, bool_oclc, bool_upc, otherauthor_count, isbn_count, primary_url_count, str(bool_isbn1_summary), str(bool_isbn1_toc), str(bool_isbn1_dbc), str(bool_isbn1_lc), str(bool_isbn1_mc), str(bool_isbn1_sc), str(bool_oclc_summary), str(bool_oclc_toc), str(bool_oclc_dbc), str(bool_oclc_lc), str(bool_oclc_mc), str(bool_oclc_sc), str(bool_upc_avsummary), str(bool_upc_toc), str(bool_upc_dbc), str(bool_upc_lc), str(bool_upc_mc), str(bool_upc_sc), str(bool_isbn2x_summary), str(bool_isbn2x_toc), str(bool_isbn2x_dbc), str(bool_isbn2x_lc), str(bool_isbn2x_mc), str(bool_isbn2x_sc)])
		
		i += 1
			
with open('MARC773s.txt', 'r') as f:
	MARC773s = f.read().splitlines()
#num_input_lines = sum(1 for line in open('MARC773s.txt'))

c = csv.writer(open("test_2-3-16-1.csv", "wb"))
c.writerow(["Collection", "UNCb Identifier", "PK", "ICE ToC", "Main Author", "OCLC Number", "UPC", "Other Authors", "Syndetics ISBNs", "Primary URLs", "ISBN1:SUMMARY", "ISBN1:TOC", "ISBN1:DBCHAPTER", "ISBN1:LC", "ISBN1:MC", "ISBN1:SC", "OCLC:SUMMARY", "OCLC:TOC", "OCLC:DBCHAPTER", "OCLC:LC", "OCLC:MC", "OCLC:SC", "UPC:AVSUMMARY", "UPC:TOC", "UPC:DBCHAPTER", "UPC:LC", "UPC:MC", "UPC:SC","ISBN2X:SUMMARY", "ISBN2X:TOC", "ISBN2X:DBCHAPTER", "ISBN2X:LC", "ISBN2x:MC", "ISBN2X:SC", "LC CLASS BOOL", "LCSH COUNT", "MESH COUNT", "OTHER SH COUNT"])

#print num_input_lines

loopThroughInputList()