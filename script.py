# This script will download XML files using the TRLN Endeca web services API, then parse it to provide data on Syndedicts provided information
# Libby Wilcher (https://github.com/libbby/Syndetics-Catalog-Coverage-Assessment)

import webbrowser 
import lxml.etree as ET
import urllib
import csv
import time


MARC773 = raw_input("enter MARC773 field: ") 					# if using PowerShell, right click to paste
MARC773 = MARC773.replace(" ", "_")
collection_short = raw_input("enter a 'shorthand' code for the collection: ")

endeca_url = "http://search.lib.unc.edu/search?Ntt=" + MARC773 + "&Ntk=Keyword&Nty=1&output-format=xml&facet-options=exclude-refinements&include-record-property=ICE+Chapter+Title&include-record-property=Syndetics+ISBN&include-record-property=OCLCNumber&include-record-property=UPC&include-record-property=Main+Author&include-record-property=Other+Authors&maximum-number-records=1000"
webbrowser.open(endeca_url) 									# here's your XML file in browser, if you want it.
urllib.urlretrieve(endeca_url, MARC773 + ".xml") 				# saves that XML into the same folder this script is in, the name is the MARC773 field

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

#c = csv.writer(open(MARC773 + ".csv", "wb"))
#c.writerow(["Collection", "UNCb Identifier", "PK", "ICE ToC", "Main Author", "OCLC Number", "UPC", "Other Authors", "Syndetics ISBNs"])

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
		
		isbnx = []
		for node in child[1][0][i][1].find('Syndetics-ISBN').iter("item"):
			isbnx.append(node.text)
			z = int(child[1][0][i][1].xpath("count(./Syndetics-ISBN/item)"))
		y=0
		z = int(child[1][0][i][1].xpath("count(./Syndetics-ISBN/item)"))
		for y in range(z):
			print isbnx[y]
			webbrowser.open("http://syndetics.com/index.aspx?isbn=" + isbnx[y] + "/XML.XML&client=ncchapelh&oclc=")
			y += 1
			time.sleep(0.001)
		
		
		#webbrowser.open("http://syndetics.com/index.aspx?isbn=" + isbnx[i] + "/XML.XML&client=ncchapelh&oclc=")
		#urllib.urlretrieve("http://syndetics.com/index.aspx?isbn=" + isbn1 + "/XML.XML&client=ncchapelh")
		
		
		print child[1][0][i][0].text + ", " + str(bool_ice_toc) + ", " + str(bool_main_author) + ", " + str(bool_oclc) + ", " + str(bool_upc) + ", " + str(int(child[1][0][i][1].xpath("count(./Other-Authors/item)"))) + ", " + str(int(child[1][0][i][1].xpath("count(./Syndetics-ISBN/item)"))) + ", " + str(isbnx)
		#c.writerow([collection_short, child[1][0][i][0].text, collection_short + child[1][0][i][0].text, bool_ice_toc, bool_main_author, bool_oclc, bool_upc, int(child[1][0][i][1].xpath("count(./Other-Authors/item)")), int(child[1][0][i][1].xpath("count(./Syndetics-ISBN/item)"))])
		


