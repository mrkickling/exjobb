from geopy.distance import distance

# Observed coarse locations, and frequency
locations = {}
records = 0


def dist(lat1, lon1, lat2, lon2):
	    return distance((lat1, lon1), (lat2, lon2))

with open('plot.csv', 'r') as f:
	for line in f.readlines():
		records += 1
		line = line.split(";")
		lat_fine = (float(line[0]))
		lon_fine = (float(line[1]))
		lat_coarse = (float(line[2]))
		lon_coarse = (float(line[3]))
		fine = (lat_fine, lon_fine)
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
distance = dist(lat_fine, lon_fine, resulting_lat, resulting_lon).m
with open("10000iterations.txt", 'a') as f:
	f.write(str(distance) + '\n')
f.close()