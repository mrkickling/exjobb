from location import Location
from GTFSreader import GTFSReader
import sys
import argparse

if len(sys.argv) > 3:
	command = sys.argv[1]
	folder = sys.argv[2]
	reader = GTFSReader(folder)

	if command == "infertrip":
		approx_route = sys.argv[3]
		reader.combined_infer_route(approx_route)
	# if command == "infertrip2":
	# 	approx_route = sys.argv[3]
	# 	reader.get_potential_routes_from_user_route(approx_route, True)
	elif command == "getshape":
		route_short_name = sys.argv[3]
		reader.get_shape_of_route(route_short_name)
	elif command == "getstops":
		route_short_name = sys.argv[3]
		reader.get_stops_of_route(route_short_name)

print("done!")