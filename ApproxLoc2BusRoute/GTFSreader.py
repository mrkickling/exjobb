import pandas as pd
from location import Location
from datetime import datetime, timedelta
import math
import copy
import os

class GTFSReader:
	folder_rel = "None"
	bus_routes = {}

	def degrees_to_radians(self, degrees):
		return degrees * math.pi / 180

	def __init__(self, folder_rel):
		self.folder_rel = folder_rel
		self.fetch_data()
		self.APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR = 111000
		self.MAX_LATITUDE = 90.0 - (1.0 / self.APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR)

	def fetch_data(self):
		self.routes_csv = pd.read_csv(self.folder_rel + '/' + 'routes.txt')
		self.shapes_csv = pd.read_csv(self.folder_rel + '/' + 'shapes.txt')
		self.trips_csv = pd.read_csv(self.folder_rel + '/' + 'trips.txt')
		self.stop_times = pd.read_csv(self.folder_rel + '/' + 'stop_times.txt')
		self.stops_csv = pd.read_csv(self.folder_rel + '/' + 'stops.txt')

	def read_route(self, userroute):
		locations = []
		with open(userroute) as f:
			for row in f.readlines()[1:]:
				values = row.split(",")
				date = (values[0])
				time = (values[1])
				loc = Location(float(values[2]), float(values[3]), date, time)
				locations.append(loc)
		locations.sort(key = lambda x : x.time)
		return locations

	def metersToDegreesLatitude(self, distance):
		return distance / self.APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR;

	def metersToDegreesLongitude(self, distance, lat):
		return distance / self.APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR / math.cos(self.degrees_to_radians(lat));

	def get_shape_of_route(self, bus_nr):
		routes_filtered_nr = self.routes_csv[(self.routes_csv.route_short_name == bus_nr)]
		route_id = routes_filtered_nr.iat[0,0]
		# Find a trip id of route
		trips_filtered = self.trips_csv[(self.trips_csv.route_id == route_id)]
		trip_id = trips_filtered["trip_id"]
		shape_id = trips_filtered["shape_id"].iloc[0]
		shapes_filtered = self.shapes_csv[(self.shapes_csv.shape_id == shape_id)]
		route = shapes_filtered[shapes_filtered.columns[1:3]]
		for index, row in route.iterrows():
		    print(str(row["shape_pt_lat"]) + "," + str(row["shape_pt_lon"]))
		    
	def get_stops_of_route(self, bus_nr):
		routes_filtered_nr = self.routes_csv[(self.routes_csv.route_short_name == bus_nr)]
		route_id = routes_filtered_nr.iat[0,0]
		# Find a trip id of route
		trips_filtered = self.trips_csv[(self.trips_csv.route_id == route_id)]
		found = False
		for i in range(len(trips_filtered)):
			trip_id = trips_filtered["trip_id"].iloc[i]
			stoptimes_filtered = self.stop_times[(self.stop_times.trip_id == trip_id)]
			stops = pd.merge(stoptimes_filtered, self.stops_csv, on="stop_id")
			if stops["arrival_time"].iloc[-1] < "24:00:00":
				break
		result = ""
		for index, row in stops.iterrows():
		    result += "date," + str(row["arrival_time"]) + "," + str(row["stop_lat"]) + "," + str(row["stop_lon"])
		    result += '\n'
		print(result)
		return result

	def output_all_bus_stops(self, folder):
		for index, row in self.routes_csv.iterrows():
			if row["route_type"] == 700: # if route is a bus
				filename = folder + "/" + row["route_short_name"] + "-" + self.folder_rel.split("/")[1] + ".csv"
				with open(filename, "w") as f:
					f.write(self.get_stops_of_route(row["route_short_name"]))
			print("done bus", row["route_short_name"])

	def dist_between(self, lat1, lon1, lat2, lon2):
		earthRadiusKm = 6371
		dLat = self.degrees_to_radians(lat2-lat1)
		dLon = self.degrees_to_radians(lon2-lon1)

		lat1 = self.degrees_to_radians(lat1)
		lat2 = self.degrees_to_radians(lat2)

		a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2);
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
		return earthRadiusKm * c;

	def dist_filter_shape(self, row, userpos):
		return self.dist_between(row["shape_pt_lat"], row["shape_pt_lon"], userpos.lat, userpos.lon) < 2
	
	def dist_filter_stop(self, row, userpos):
		return self.dist_between(row["stop_lat"], row["stop_lon"], userpos.lat, userpos.lon) < 2

	def unique_items(self, l):
		seen = {}
		result = []
		for item in l:
			if not item in seen:
				seen[item] = True
				result.append(item)
		return result
	
	def route_nr_from_shape(self, shape_id):
		trips = self.trips_csv[(self.trips_csv["shape_id"] == shape_id)]
		if not trips.empty:
			route_id = trips["route_id"].iloc[0]
			routes = self.routes_csv[(self.routes_csv["route_id"] == route_id)]
			unique_nrs = routes.route_short_name.unique()
			return unique_nrs[0]
		else:
			return None

	def route_id_from_shape(self, shape_id):
		print("shapeid:", str(shape_id))
		print("shapeid:", shape_id)
		trips = self.trips_csv[(self.trips_csv["shape_id"] == shape_id)]
		if not trips.empty:
			route_id = trips["route_id"].iloc[0]
			return route_id
		else:
			return None

	def route_nrs_from_shapes(self, shapes):
		result = []
		for shape_id in shapes:
			route_nr = self.route_nr_from_shape(shape_id)
			if route_nr is not None:
				result.append(route_nr)
		return self.unique_items(result)

	def route_ids_from_shapes(self, shapes):
		result = []
		for shape_id in shapes:
			route_id = self.route_id_from_shape(shape_id)
			if route_id is not None:
				result.append(route_id)
		return self.unique_items(result)

	def most_common_in_frequency_table(self, frequency_table):
		max_val = 0
		max_keys = None
		for key in frequency_table:
			val = frequency_table[key]
			if val > max_val:
				max_val = val
				max_keys = [key]
			elif val == max_val:
				max_keys.append(key)
		return max_keys

	# Return routes that match an approximate user position
	# considering the location and stop times for a bus/train trip
	def get_potential_bus_stops_for_user_pos(self, userpos, trips, dist_max = 2):
		print(userpos.time, userpos.lat, userpos.lon)
		f = '%H:%M:%S'
		time_start = datetime.strptime(userpos.time, f) - timedelta(minutes=5)
		time_end = datetime.strptime(userpos.time, f) + timedelta(minutes=5)
		time_start = time_start.strftime(f)
		time_end = time_end.strftime(f)

		trips_and_stoptimes = trips.merge(self.stop_times,on='trip_id')
		trips_and_stoptimes = pd.merge(trips_and_stoptimes, self.stops_csv,on='stop_id')
		filter_dist = trips_and_stoptimes.apply(self.dist_filter_stop, axis=1, userpos=userpos)
		filtered_stop_times = trips_and_stoptimes[filter_dist]
		filtered_stop_times = filtered_stop_times[((filtered_stop_times.arrival_time >= time_start) & (filtered_stop_times.arrival_time <= time_end))]
		filtered_stop_times = pd.merge(filtered_stop_times, self.routes_csv,on='route_id')

		potentials = []
		for index, row in filtered_stop_times.iterrows():
			if row["route_short_name"] not in potentials:
				potentials.append(row["route_short_name"])
		return potentials

	# Find trips that match the userroute and route ids
	# using self.get_potential_bus_stops_for_user_pos
	def get_potential_trips_from_user_route(self, userroute, route_ids):
		filtered_trips = self.trips_csv[self.trips_csv["route_id"].isin(route_ids)]
		print("route ids", route_ids)

		frequency_table_route_nr = {} # route_nr to frequency of matching stops
		seen_locs = []
		# Go through each location in the user route and check if they match stop times
		for loc in userroute:
			if str(loc) in seen_locs:
				print("Skipping seen location")
				continue
			seen_locs.append(str(loc))
			res = self.get_potential_bus_stops_for_user_pos(loc, filtered_trips)
			for route_nr in res:					
				if route_nr in frequency_table_route_nr:
					frequency_table_route_nr[route_nr] += 1
				else:
					frequency_table_route_nr[route_nr] = 1

		return frequency_table_route_nr

	# input - userpost: Location, seen_prev: list<shape_id>, seen_before_prev: list<shape_id>
	# Return all shapes that match the current location and have been seen before
	# return - list<shape_id>
	def get_potential_shapes_for_user_pos(self, userpos, freq_shape_id):
		print(userpos.time, userpos.lat, userpos.lon)
		if len(freq_shape_id) > 0:
			mask = (self.shapes_csv["shape_id"].isin(freq_shape_id.keys()))
			self.shapes_csv = self.shapes_csv[mask]
		
		filter_dist = self.shapes_csv.apply(self.dist_filter_shape, axis=1, userpos=userpos)
		filtered_shapes = self.shapes_csv[filter_dist]
		potentials = filtered_shapes.shape_id.unique().tolist()
		
		for shape_id in potentials:
			if shape_id in freq_shape_id:
				freq_shape_id[shape_id] += 1
			else:
				freq_shape_id[shape_id] = 1

	# input - userroute:string relative path to the users approximate route
	# Iterate through each location in userroute and find shapes matching
	# all the locations by using self.get_potential_routes_for_user_pos 
	# return: dict{shape id:num matches in userroute}
	def get_potential_shapes_for_user_route(self, userroute):
		freq_shape_id = {}
		seen_locs = []
		for loc in userroute:				
			if str(loc) in seen_locs:
				print("Skipping location that has been seen before...")
				# If the potential shapes already calculated
				continue
			seen_locs.append(str(loc))
			self.get_potential_shapes_for_user_pos(loc, freq_shape_id)
		return freq_shape_id

	# userroute: a path to a csv with approximate locations (see folder routes)
	# By using GTFS data the program attempts to find the most probable trip and route
	# for the user route, by using the stop times and locations of the bus/train trips
	# return: the most probable route (line number) that the userroute matches
	def combined_infer_route(self, userroute):
		userroute = self.read_route(userroute)

		print("Starting shape inference. This will take a while.")
		# Get all potential shapes for userroute rated after how well they match
		freq_dict_shape_id = self.get_potential_shapes_for_user_route(userroute)
		
		# Get the shapes that matches best for the user route
		potential_shapes = self.most_common_in_frequency_table(freq_dict_shape_id)
		
		# Convert shapes to route_ids
		potential_routes = self.route_ids_from_shapes(potential_shapes)
		
		print("potential routes", self.route_nrs_from_shapes(potential_shapes))
		print("Starting bus stop time inference")
		frequency_table_route_nr = self.get_potential_trips_from_user_route(userroute, potential_routes)
		print(frequency_table_route_nr)
		print("Most probable route(s):", self.most_common_in_frequency_table(frequency_table_route_nr))
		result = self.most_common_in_frequency_table(frequency_table_route_nr)		
		return str(result)
	
	def infer_all_in_directory(self, indir, outdir):
		in_files = os.listdir(indir)
		out_files = os.listdir(outdir)
		for file in in_files:
			file_path = indir + "/" + file
			print(file)
			if file in out_files:
				print("Already done this file")
				continue
			try:
				result = self.combined_infer_route(file_path)
			except:
				print("Something went wrong with", file)
				result = ""
			with open(outdir + "/" + file, "w") as f:
				f.write(result)
			self.fetch_data()
