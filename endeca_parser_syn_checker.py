# This script will download XML files using the TRLN Endeca web services API and then parse them for data 'match-points' to search for Syndetics matches.
# Results are written to a CSV file in the same directory script lives in
# Libby Wilcher (https://github.com/libbby/Syndetics-Catalog-Coverage-Assessment), UNC Chapel Hill
# Script written and tested in Python 2.7
# Script uses lxml library available at https://pypi.python.org/pypi/lxml/3.4.4
# Last updated: 5 May 2016

#		INSTRUCTIONS:
#	 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#	|																									|
#	|	1.) You will need the lxml library installed in your Python27\Lib directory. 					|
#	|		Find the appropriate copy for your machine here: https://pypi.python.org/pypi/lxml/3.4.4	|
#	|	2.) You will need a text file named BNums.txt in the same directory this script is stored.		|
#	|		Each line of the file must contain one (1) b-num of the format bXXXXXXX. Do not include 	|
#	|		opening or trailing spaces.																	|
#	|	3.) You will need a CSV named ____.csv in the same directory this script is stored. 			|
#	|		This CSV must be the output from the perl script ____.pl.									|
#	|	3.)	If, for whatever reason, you want each Endeca XML result opened in your web browser,		|
#	|		un-comment line __.																			|
#	|	4.) DO NOT remove the sleep time on line __. Bad things will probably happen, and your results	|
#	|		will be retrieved from Endeca progressively slower.											|
#	|	5.) This output from this script will be saved as a CSV file.									|
#	|																									|
#	 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import webbrowser 
import lxml.etree as ET
import lxml.html as HTML
import urllib
import csv
import time

def isEbook(): # test for determing if item is an ebook
	global format_list
	format_list = []
	global bool_is_ebook
	subtotal_bool_is_ebook = 0
	f = 0
	fn = child.xpath('//Format/dimensionValues/item/name')
	for name in fn: #name in child.xpath('//Format/dimensionValues/item/name'):
		format_list.append(name.text)
		if format_list[f] == "eBook":
			bool_is_ebook = 1
		else:
			bool_is_ebook = 0
		subtotal_bool_is_ebook += bool_is_ebook
		f += 1
	if subtotal_bool_is_ebook > 0:
		bool_is_ebook = 1
	else:
		bool_is_ebook = 0

def populateISBN():
	global isbn_list
	isbn_list = []
	ix = child.xpath('//fullRecordsList/item/properties/Syndetics-ISBN/item')
	for item in ix:
		isbn_list.append(item.text)
def isbn1SyndTest():
	global bool_isbn1_summary
	global bool_isbn1_toc
	global bool_isbn1_dbc
	global bool_isbn1_lc
	global bool_isbn1_mc
	global bool_isbn1_sc
	if len(isbn_list) > 0:
		syn_doch_isbn1 = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[0] + "/XML.XML&client=ncchapelh")) # for missing Syndetics results, parse them as HTML
		if syn_doch_isbn1.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
			bool_isbn1_summary = 0
			bool_isbn1_toc = 0
			bool_isbn1_dbc = 0
			bool_isbn1_lc = 0
			bool_isbn1_mc = 0
			bool_isbn1_sc = 0
		else:
			syn_docx_isbn1 = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[0] + "/XML.XML&client=ncchapelh")) # parse the Syndetics results as XML, because there were not HTML tags present.
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
	else:
		bool_isbn1_summary = 0 # filter the CSV to differentiate items whose ISBN returns no Synetics info and items who do not HAVE ISBNs
		bool_isbn1_toc = 0
		bool_isbn1_dbc = 0
		bool_isbn1_lc = 0
		bool_isbn1_mc = 0
		bool_isbn1_sc = 0

def oclcSynTest(): # use this function on each ITEM in the Endeca XML to search for Syndetics info using the OCLC number listed.
	global bool_oclc_avsummary
	global bool_oclc_toc
	global bool_oclc_dbc
	global bool_oclc_lc
	global bool_oclc_mc
	global bool_oclc_sc
	#if bool_is_ebook == 0:
	if oclc_number == '':
		bool_oclc_avsummary = 0
		bool_oclc_toc = 0
		bool_oclc_dbc = 0
		bool_oclc_lc = 0
		bool_oclc_mc = 0
		bool_oclc_sc = 0
	else:
		syn_doch_oclc = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(oclc_number))) # for missing Syndetics results, parse them as HTML
		if syn_doch_oclc.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
			bool_oclc_avsummary = 0
			bool_oclc_toc = 0
			bool_oclc_dbc = 0
			bool_oclc_lc = 0
			bool_oclc_mc = 0
			bool_oclc_sc = 0
		else:
			syn_docx_oclc = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(oclc_number)))
			if syn_docx_oclc.find('AVSUMMARY') != None: # Searches Syndetics XML for a 'SUMMARY' tag
				bool_oclc_avsummary = 1
			else:
				bool_oclc_avsummary = 0 
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
			#urllib.urlretrieve("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + oclc_number[0]
		
	#else:
	#	bool_oclc_summary = "null"
	#	bool_oclc_toc = "null" 
	#	bool_oclc_dbc = "null" 
	#	bool_oclc_lc = "null"
	#	bool_oclc_mc = "null"
	#	bool_oclc_sc = "null"
	
def upcSynTest(): # use this function on each ITEM in the Endeca XML to search for Syndetics info using the OCLC number listed.
	global bool_upc_avsummary
	global bool_upc_toc
	global bool_upc_dbc
	global bool_upc_lc
	global bool_upc_mc
	global bool_upc_sc
	#if bool_is_ebook == 0:
	if upc_number == '':
		bool_upc_avsummary = 0
		bool_upc_toc = 0
		bool_upc_dbc = 0
		bool_upc_lc = 0
		bool_upc_mc = 0
		bool_upc_sc = 0
	else:
		syn_doch_upc = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=&upc=" + str(upc_number) + "/XML.XML&client=ncchapelh")) # for missing Syndetics results, parse them as HTML
		if syn_doch_upc.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
			bool_upc_avsummary = 0
			bool_upc_toc = 0
			bool_upc_dbc = 0
			bool_upc_lc = 0
			bool_upc_mc = 0
			bool_upc_sc = 0
		else:
			syn_docx_upc = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=&upc=" + str(upc_number) + "/XML.XML&client=ncchapelh"))
			if syn_docx_upc.find('AVSUMMARY') != None: # Searches Syndetics XML for a 'SUMMARY' tag
				bool_upc_avsummary = 1
			else:
				bool_upc_avsummary = 0 
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
			#urllib.urlretrieve("http://syndetics.com/index.aspx?isbn=&upc=" + upc_number[0] + "/XML.XML&client=ncchapelh")
		
	#else:
	#	bool_upc_avsummary = "null"
	#	bool_upc_toc = "null" 
	#	bool_upc_dbc = "null" 
	#	bool_upc_lc = "null"
	#	bool_upc_mc = "null"
	#	bool_upc_sc = "null"
	
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
	z = len(isbn_list)	# the number of ISBNs associated with the particular item
	if z > 1:	
		for y in range(z):	# loops through each ISBN
			if y > 0:	# y = 0 is our ISBN1, we already did that one
				syn_doch_isbn2x = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[y] + "/XML.XML&client=ncchapelh"))	# for missing Syndetics results, parse them as HTML
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
					syn_docx_isbn2x = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[y] + "/XML.XML&client=ncchapelh"))
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
			
def loopThroughInputList():
	global il
	il = 0
	global BNum
	global child
	global collection_short
	
	while il < len(BNums):
		BNum = BNums[il]
		endeca_url = "http://search.lib.unc.edu/search?R=UNC"+BNum+"&output-format=xml&record-options=include-record-facets"
		#webbrowser.open(endeca_url)	# here's your XML file in browser, if you want it.
		urllib.urlretrieve(endeca_url, 'BNum_XMLs/' + BNum + '.xml')	# saves that XML into the XML folder
		
		tree = ET.parse('BNum_XMLs/' + BNum + '.xml')	# set up XML tree to parse
		root = tree.getroot()
		for child in root:	# tells us (and script) what child is
			root.iter()
		
		parseXML()
		
		il += 1
		time.sleep(2.0)

def parseXML():
	global i
	global format_count
	global oclc_number
	global upc_number
	i = 0
	
	isbn_count = int(child.xpath('count(//Syndetics-ISBN/item)'))
	otherauthor_count = int(child.xpath('count(//Other-Authors/item)'))
	primary_url_count = int(child.xpath('count(//Primary-URL/item)'))
	format_count = int(child.xpath('count(//Format/dimensionValues/item)'))
	isEbook()
	populateISBN()
		
	ice_toc = int(child.xpath('count(//ICE-Chapter-Title)'))
	if ice_toc > 0:
		bool_ice_toc = 1
	else:
		bool_ice_toc = 0
				
	main_author = int(child.xpath('count(//Main-Author)'))
	if main_author > 0:
		bool_main_author = 1
	else:
		bool_main_author = 0

	oclc_number = child.xpath('//fullRecordsList/item/properties/OCLCNumber/item/text()')
	if oclc_number != '':
		bool_oclc = 1
	else:
		bool_oclc = 0
				
	upc_number = child.xpath('//fullRecordsList/item/properties/UPC/item/text()')
	if upc_number != '':
		bool_upc = 1
	else:
		bool_upc = 0
		
		#populateISBN()
	isbn1SyndTest()
	time.sleep(1.0)
	oclcSynTest()
	time.sleep(1.0)
	upcSynTest()
	time.sleep(1.0)
	isbn2xSynTest()
			
		
		#c.writerow([collection_short, child[1][1][i][1].text, collection_short + child[1][1][i][1].text, bool_ice_toc, bool_main_author, bool_oclc, bool_upc, otherauthor_count, isbn_count, primary_url_count, str(bool_isbn1_summary), str(bool_isbn1_toc), str(bool_isbn1_dbc), str(bool_isbn1_lc), str(bool_isbn1_mc), str(bool_isbn1_sc), str(bool_oclc_summary), str(bool_oclc_toc), str(bool_oclc_dbc), str(bool_oclc_lc), str(bool_oclc_mc), str(bool_oclc_sc), str(bool_upc_avsummary), str(bool_upc_toc), str(bool_upc_dbc), str(bool_upc_lc), str(bool_upc_mc), str(bool_upc_sc), str(bool_isbn2x_summary), str(bool_isbn2x_toc), str(bool_isbn2x_dbc), str(bool_isbn2x_lc), str(bool_isbn2x_mc), str(bool_isbn2x_sc)])
	
	#print(BNum, isbn_count, bool_ice_toc, bool_main_author, otherauthor_count, primary_url_count, format_count, format_list, bool_is_ebook, bool_oclc, oclc_number, bool_upc, upc_number, isbn_list)
	print(BNum, bool_isbn1_summary, bool_isbn1_toc, bool_isbn1_dbc, bool_isbn1_lc, bool_isbn1_mc, bool_isbn1_sc)
	#print(BNum, bool_oclc_avsummary, bool_oclc_toc, bool_oclc_dbc, bool_oclc_lc, bool_oclc_mc, bool_oclc_sc)
	#print(BNum, bool_upc_avsummary, bool_upc_toc, bool_upc_dbc, bool_upc_lc, bool_upc_mc, bool_upc_sc)
	print(BNum, bool_isbn2x_summary, bool_isbn2x_toc, bool_isbn2x_dbc, bool_isbn2x_lc, bool_isbn2x_mc, bool_isbn2x_sc)
	i += 1		
		
with open('BNums.txt', 'r') as f:
	BNums = f.read().splitlines()

#c = csv.writer(open("python_output.csv", "wb"))
#c.writerow(["Collection", "UNCb Identifier", "PK", "ICE ToC", "Main Author", "OCLC Number", "UPC", "Other Authors", "Syndetics ISBNs", "Primary URLs", "ISBN1:SUMMARY", "ISBN1:TOC", "ISBN1:DBCHAPTER", "ISBN1:LC", "ISBN1:MC", "ISBN1:SC", "OCLC:SUMMARY", "OCLC:TOC", "OCLC:DBCHAPTER", "OCLC:LC", "OCLC:MC", "OCLC:SC", "UPC:AVSUMMARY", "UPC:TOC", "UPC:DBCHAPTER", "UPC:LC", "UPC:MC", "UPC:SC","ISBN2X:SUMMARY", "ISBN2X:TOC", "ISBN2X:DBCHAPTER", "ISBN2X:LC", "ISBN2x:MC", "ISBN2X:SC", "LC CLASS BOOL", "LCSH COUNT", "MESH COUNT", "OTHER SH COUNT"])

loopThroughInputList()
