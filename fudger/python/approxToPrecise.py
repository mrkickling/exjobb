from geopy.distance import distance
import sys

# Observed coarse locations, and frequency
locations = {}
records = 0


def dist(lat1, lon1, lat2, lon2):
    return distance((lat1, lon1), (lat2, lon2))


# Go through each line in std in
# In file is expected to be a file of precise locations
for line in sys.stdin:
    records += 1
    line = line.split(";")

    lat_fine = float(line[0])
    lon_fine = float(line[1])

    lat_coarse = float(line[2])
    lon_coarse = float(line[3])

    fine = (lat_fine, lon_fine)
    coarse = (lat_coarse, lon_coarse)

    # Add frequencies to dictionary
    if coarse in locations:
        locations[coarse] += 1
    else:
        locations[coarse] = 1

resulting_lat = 0
resulting_lon = 0

# Calculate the averaged location using the frequencies
for location in locations:
    locations[location] = locations[location] / records
    resulting_lat += location[0] * locations[location]
    resulting_lon += location[1] * locations[location]

distance = dist(lat_fine, lon_fine, resulting_lat, resulting_lon).m
print(str(distance))
