# This script will download XML files using the TRLN Endeca web services API, then parse it to provide data on Syndedicts provided information
# Libby Wilcher (https://github.com/libbby/Syndetics-Catalog-Coverage-Assessment)

import webbrowser 
import xml.etree.ElementTree as ET
import urllib
import csv


MARC773 = raw_input("enter MARC773 field: ") 					# if using PowerShell, right click to paste
MARC773 = MARC773.replace(" ", "_")

endeca_url = "http://search.lib.unc.edu/search?Ntt=" + MARC773 + "&Ntk=Keyword&Nty=1&output-format=xml&facet-options=exclude-refinements&include-record-property=ICE+Chapter+Title&include-record-property=Syndetics+ISBN&include-record-property=OCLCNumber&include-record-property=UPC&include-record-property=Main+Author&include-record-property=Other+Authors&maximum-number-records=1000"
webbrowser.open(endeca_url) # here's your XML file in browser, if you want it. Firefox allows spaces from MARC773.
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

c = csv.writer(open(MARC773 + ".csv", "wb"))

for node in child[0]:											
	for i in range(n):											# this cycles through the ITEM tags that contain records data
		if child[1][0][i][1][0].tag == "ICE-Chapter-Title":		# sets variable ICE_TOC to y/n
			ICE_TOC = "1"
		else:
			ICE_TOC = "0"
			
		if child[1][0][i][1][0].tag == "Main-Author":
			Main_Author = "1"
		elif child[1][0][i][1][1].tag == "Main-Author":
			Main_Author = "1"
		elif child[1][0][i][1][2].tag == "Main-Author":
			Main_Author = "1"
		else:
			Main_Author = "0"
			
		if child[1][0][i][1][0].tag == "OCLCNumber":
			OCLC_Number = "1"
		elif child[1][0][i][1][1].tag == "OCLCNumber":
			OCLC_Number = "1"
		elif child[1][0][i][1][2].tag == "OCLCNumber":
			OCLC_Number = "1"
		else:
			OCLC_Number = "0"
		
		c.writerow([child[1][0][i][0].text, ICE_TOC, Main_Author, OCLC_Number])			# comma delimited output... ADD TO THIS

