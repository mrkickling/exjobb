class Location:
	lat = 0
	lon = 0

	def __init__(self, lat, lon, date, time):
		self.lat = lat
		self.lon = lon
		self.date = date
		self.time = time
	
	def __str__(self): 
		return "%s, %s" % (self.lat, self.lon)

	def add_to_lat(self, deg):
		self.lat += deg

	def add_to_lon(self, deg):
		self.lon += deg