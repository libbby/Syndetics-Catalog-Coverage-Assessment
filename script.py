# This script will download XML files using the TRLN Endeca web services API, then parse it to provide data on Syndedicts provided information
# Libby Wilcher (https://github.com/libbby/Syndetics-Catalog-Coverage-Assessment)

import webbrowser 
import xml.etree.ElementTree as ET
import urllib
import csv


MARC773 = raw_input("enter MARC773 field: ") 					# if using PowerShell, right click to paste
MARC773 = MARC773.replace(" ", "_")

endeca_url = "http://search.lib.unc.edu/search?Ntt=" + MARC773 + "&Ntk=Keyword&Nty=1&output-format=xml&facet-options=exclude-refinements&include-record-property=ICE+Chapter+Title&include-record-property=Syndetics+ISBN&include-record-property=OCLCNumber&include-record-property=UPC&include-record-property=Main+Author&include-record-property=Other+Authors&maximum-number-records=1000"
#webbrowser.open(endeca_url) # here's your XML file in browser, if you want it. Firefox allows spaces from MARC773.
urllib.urlretrieve(endeca_url, MARC773 + ".xml") 				# saves that XML into the same folder this script is in, the name is the MARC773 field

tree = ET.parse(MARC773 + ".xml")
# tree = ET.parse("search.xml") #test case for Kristina's UPC xml
root = tree.getroot()

for child in root: 												# tells us (and script) what child is
	root.iter()

for node in child: 												# tells us (and script) what node is
	child.iter()
	
n = 0															# produces a count of ebooks in the given collection
for node in child[1][0]:
	n += 1

print ("There are " + str(n) + " ebooks in this collection.")

c = csv.writer(open(MARC773 + ".csv", "wb"))
# c = csv.writer(open("search.csv", "wb")) #test case for Kristina's UPC xml

for node in child[0]:											
	for i in range(n):											# this cycles through the ITEM tags that contain records data
		ice_toc = child[1][0][i][1].find('ICE-Chapter-Title')
		if ice_toc != None:
			bool_ice_toc = 1
		else:
			bool_ice_toc = 0
			
		main_author = child[1][0][i][1].find('Main-Author')
		if main_author != None:
			bool_main_author = 1
		else:
			bool_main_author = 0
			
		upc = child[1][0][i][1].find('UPC')
		if upc != None:
			bool_upc = 1
		else:
			bool_upc = 0
			
		oclc_number = child[1][0][i][1].find('OCLCNumber')
		if oclc_number != None:
			bool_oclc = 1
		else:
			bool_oclc = 0
				
		print child[1][0][i][0].text + ", " + str(bool_ice_toc) + ", " + str(bool_main_author) + ", " + str(bool_oclc) + ", " + str(bool_upc)
		c.writerow([child[1][0][i][0].text, bool_ice_toc, bool_main_author, bool_oclc, bool_upc])		# comma delimited output... ADD TO THIS
		


