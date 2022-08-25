from location import Location
from GTFSreader import GTFSReader
import sys
import argparse

def help():
	print("main.py [infertrip|getshape|getstops|getallstops] [gtfs_path] [output_path|route_path] [output_path]")

if len(sys.argv) > 3:
	command = sys.argv[1]
	gtfs_folder = sys.argv[2]
	reader = GTFSReader(gtfs_folder)

	if command == "infertrip":
		approx_route = sys.argv[3]
		reader.combined_infer_route(approx_route)
	elif command == "infertrips": # Performing inference on all files in a directory
		approx_route_dir = sys.argv[3]
		out_dir = sys.argv[4]
		reader.infer_all_in_directory(approx_route_dir, out_dir)
	elif command == "getshape":
		route_short_name = sys.argv[3]
		reader.get_shape_of_route(route_short_name)
	elif command == "getstops":
		route_short_name = sys.argv[3]
		reader.get_stops_of_route(route_short_name)
	elif command == "getallstops":
		out_folder = sys.argv[3] # output to folder
		reader.output_all_bus_stops(out_folder)
	else:
		help()
else:
	help()