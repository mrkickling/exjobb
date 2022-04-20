import sys
from lxml import etree
import csv 

fields = ["session", "lat", "lon", "data", "time"];
rows = []
filename = sys.argv[1]
sessionname = sys.argv[2]

doc = etree.parse(filename)
root = doc.getroot()
for child in root[4][4]:
	rows.append([
		sessionname,
		child.attrib["lat"],
		child.attrib["lon"],
		"OSM",
		child[1].text
		])

# writing to csv file 
csvwriter = csv.writer(sys.stdout) 
    
# writing the fields 
csvwriter.writerow(fields) 
    
# writing the data rows 
csvwriter.writerows(rows)