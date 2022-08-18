# Class with the purpose of mapping approximate routes to 
# possible corresponding public transport routes, using public GTFS data

class LocationFudger:
	def degrees_to_radians(self, degrees):
		return degrees * math.pi / 180

	def __init__(self):
		self.APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR = 111000
		self.MAX_LATITUDE = 90.0 - (1.0 / self.APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR)

	def wrapLatitude(self, lat):
		if lat > self.MAX_LATITUDE:
			lat = self.MAX_LATITUDE
		if lat < -self.MAX_LATITUDE:
			lat = -self.MAX_LATITUDE
		return lat

	def wrapLongitude(self, lon):
		lon %= 360.0
		if lon >= 180.0:
			lon -= 360.0
		if lon < -180.0:
			lon += 360.0
		return lon

	def metersToDegreesLatitude(self, distance):
		return distance / self.APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR;

	def metersToDegreesLongitude(self, distance, lat):
		return distance / self.APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR / math.cos(self.degrees_to_radians(lat));

	def round_locations(self, locations, accuracy):
		result = []
		for location in locations:
			result.append(round_location(location, accuracy))
		return result

	def round_location(self, location, accuracy):
		latitude = location.lat
		longitude = location.lon
		latGranularity = self.metersToDegreesLatitude(accuracy);
		latitude = self.wrapLatitude(round(latitude / latGranularity) * latGranularity);
		lonGranularity = self.metersToDegreesLongitude(accuracy, latitude);
		longitude = self.wrapLongitude(round(longitude / lonGranularity) * lonGranularity);
		return Location(latitude, longitude)
