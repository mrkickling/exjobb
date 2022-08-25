from geopy.distance import distance
import sys
# Observed coarse locations, and frequency
locations = {}
records = 0


def dist(lat1, lon1, lat2, lon2):
	    return distance((lat1, lon1), (lat2, lon2))

for line in sys.stdin:
	print(line)
	records += 1
	line = line.split(",")
	lat_coarse = (float(line[2]))
	lon_coarse = (float(line[3]))
	coarse = (lat_coarse, lon_coarse)
	if coarse in locations:
		locations[coarse] += 1
	else:
		locations[coarse] = 1

resulting_lat = 0
resulting_lon = 0

for location in locations:
	locations[location] = locations[location] / records
	resulting_lat += location[0] * locations[location]
	resulting_lon += location[1] * locations[location]

#print(locations)
#print("result", resulting_lat, resulting_lon)
#print("actual", lat_fine, lon_fine)
print(resulting_lat, resulting_lon)
