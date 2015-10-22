# This script will download XML files using the TRLN Endeca web services API, then parse it to provide data on Syndedicts provided information
# Libby Wilcher (https://github.com/libbby/Syndetics-Catalog-Coverage-Assessment)

import webbrowser 
import lxml.etree as ET
import lxml.html as HTML
import urllib
import csv
import time

def isbn1SyndTest(): # use this function on each ITEM in the Endeca XML to search for Syndetics info using the first Syndetics ISBN listed.
	global bool_isbn1_summary
	global bool_isbn1_toc
	global bool_isbn1_dbc
	global bool_isbn1_lc
	global bool_isbn1_mc
	global bool_isbn1_sc
	syn_doch_isbn1 = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbnx[0] + "/XML.XML&client=ncchapelh")) # for missing Syndetics results, parse them as HTML
	if syn_doch_isbn1.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags)
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
			
def oclcSynTest(): # use this function on each ITEM in the Endeca XML to search for Syndetics info using the OCLC number listed.
	global bool_oclc_summary
	global bool_oclc_toc
	global bool_oclc_dbc
	global bool_oclc_lc
	global bool_oclc_mc
	global bool_oclc_sc
	syn_doch_oclc = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(child[1][0][i][1].find('OCLCNumber/item').text))) # for missing Syndetics results, parse them as HTML
	if syn_doch_oclc.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags)
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

MARC773 = raw_input("enter MARC773 field: ") 
MARC773 = MARC773.replace(" ", "_")
collection_short = raw_input("enter a 'shorthand' code for the collection: ")

endeca_url = "http://search.lib.unc.edu/search?Ntt=" + MARC773 + "&Ntk=Keyword&Nty=1&output-format=xml&facet-options=exclude-refinements&include-record-property=ICE+Chapter+Title&include-record-property=Syndetics+ISBN&include-record-property=OCLCNumber&include-record-property=UPC&include-record-property=Main+Author&include-record-property=Other+Authors&maximum-number-records=1000"
webbrowser.open(endeca_url) 									# here's your XML file in browser, if you want it.
urllib.urlretrieve(endeca_url, MARC773 + ".xml") 				# saves that XML into the same folder this script is in, the name is the MARC773 field
c = csv.writer(open(MARC773 + ".csv", "wb"))
c.writerow(["Collection", "UNCb Identifier", "PK", "ICE ToC", "Main Author", "OCLC Number", "UPC", "Other Authors", "Syndetics ISBNs", "ISBN1:SUMMARY", "ISBN1:TOC", "ISBN1:DBCHAPTER", "ISBN1:LC", "ISBN1:MC", "ISBN1:SC", "OCLC:SUMMARY", "OCLC:TOC", "OCLC:DBCHAPTER", "OCLC:LC", "OCLC:MC", "OCLC:SC"])

tree = ET.parse(MARC773 + ".xml")
root = tree.getroot()

for child in root: 												# tells us (and script) what child is
	root.iter()
for node in child: 												# tells us (and script) what node is
	child.iter()
	
n = 0															# produces a count of ebooks in the given collection
for node in child[1][0]:
	n += 1
print ("There are " + str(n) + " ebooks in this collection.")


for node in child[0]:											
	for i in range(n):											# this cycles through the ITEM tags that contain records data
		ice_toc = child[1][0][i][1].find('ICE-Chapter-Title')
		if ice_toc != None:										# if the tag ICE-Chapter-Title is not absent (that is, it IS present) Bool =1
			bool_ice_toc = 1
		else:													# if the tag is absent, Bool =0
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
		
		isbnx = []												# creates a list of Syndetics ISBNs for each item.
		contains_isbn = child[1][0][i][1].find('Syndetics-ISBN')
		if contains_isbn != None:
			for node in child[1][0][i][1].find('Syndetics-ISBN').iter("item"):
				isbnx.append(node.text)
		else:
			isbnx.append("unavailable")
			
		isbn1SyndTest()
		time.sleep(0.0001)
		oclcSynTest()
		time.sleep(0.0001)
			
		#webbrowser.open("http://syndetics.com/index.aspx?isbn=" + isbnx[0] + "/XML.XML&client=ncchapelh&oclc=")
				
		#print "http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc="+str(child[1][0][i][1].find('OCLCNumber/item').text)
		#print child[1][0][i][0].text + ", " + str(bool_ice_toc) + ", " + str(bool_main_author) + ", " + str(bool_oclc) + ", " + str(bool_upc) + ", " + str(int(child[1][0][i][1].xpath("count(./Other-Authors/item)"))) + ", " + str(int(child[1][0][i][1].xpath("count(./Syndetics-ISBN/item)"))) + ", " + str(isbnx[0]) + ", " + str(bool_isbn1_summary) + ", " + str(bool_isbn1_toc) + ", " + str(bool_isbn1_dbc) + ", " + str(bool_isbn1_lc) + ", " + str(bool_isbn1_mc) + ", " + str(bool_isbn1_sc) + ", " + str(bool_oclc_summary) + ", " + str(bool_oclc_toc) + ", " + str(bool_oclc_dbc) + ", " + str(bool_oclc_lc) + ", " + str(bool_oclc_mc) + ", " + str(bool_oclc_sc)
		c.writerow([collection_short, child[1][0][i][0].text, collection_short + child[1][0][i][0].text, bool_ice_toc, bool_main_author, bool_oclc, bool_upc, int(child[1][0][i][1].xpath("count(./Other-Authors/item)")), int(child[1][0][i][1].xpath("count(./Syndetics-ISBN/item)")), str(bool_isbn1_summary), str(bool_isbn1_toc), str(bool_isbn1_dbc), str(bool_isbn1_lc), str(bool_isbn1_mc), str(bool_isbn1_sc), str(bool_oclc_summary), str(bool_oclc_toc), str(bool_oclc_dbc), str(bool_oclc_lc), str(bool_oclc_mc), str(bool_oclc_sc)])
		


