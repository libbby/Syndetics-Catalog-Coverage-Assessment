# This script will download XML files using the TRLN Endeca web services API, then parse it to provide data on Syndedicts provided information

import webbrowser 
import xml.etree.ElementTree as ET
import urllib

MARC773 = raw_input("enter MARC773 field: ") # if using PowerShell, right click to paste
endeca_url = "http://search.lib.unc.edu/search?Ntt=" + MARC773 + "&Ntk=Keyword&Nty=1&output-format=xml&facet-options=exclude-refinements&include-record-property=ICE+Chapter+Title&include-record-property=Syndetics+ISBN&include-record-property=OCLCNumber&include-record-property=UPC&include-record-property=Main+Author&include-record-property=Other+Authors&maximum-number-records=1000"


webbrowser.open(endeca_url) # here's your XML file in browser, if you want it. Firefox allows spaces from MARC773.

urllib.urlretrieve(endeca_url, str(MARC773)) # saves that XML into the same folder this script is in, the name is the MARC773 field



# req = urllib.request.Request(endeca_url)
# response = urllib.request.urlopen(req)
# f = open(')

# tree = ET.parse(endeca_url)
# print tree.findtext("searchTerms")

