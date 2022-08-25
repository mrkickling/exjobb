import os
import sys

def get_stats(indir):
	in_files = os.listdir(indir)

	total_buses = len(in_files)
	wrong = 0
	non_ambigious = 0
	two_ambigious = 0
	three_ambigious = 0
	more_than_3_ambigious = 0

	for filename in in_files:
		path = indir + "/" + filename
		with open(path) as f:
			bus_number = filename.split("-")[0]
			potential_routes = f.read().replace(" ", "").replace("[","").replace("]","").replace("'", "").split(",")
			if bus_number in potential_routes:
				print(bus_number, "was in", potential_routes)
				num_potentials = len(potential_routes)
				if num_potentials == 1:
					non_ambigious += 1
				elif num_potentials == 2:
					two_ambigious += 1
				elif num_potentials == 3:
					three_ambigious += 1
				elif num_potentials > 3:
					more_than_3_ambigious += 1
			else:
				print(bus_number, "was not in", potential_routes)
				wrong += 1
	print("Non ambigious:", non_ambigious, "%:", 100 * non_ambigious/total_buses)
	print("2 ambigious:", two_ambigious, "%:", 100 * two_ambigious/total_buses)
	print("3 ambigious:", three_ambigious, "%:", 100 * three_ambigious/total_buses)
	print("> 3 ambigious:", more_than_3_ambigious, "%:", 100 * more_than_3_ambigious/total_buses)
	print("wrong:", wrong, "%:", 100 * wrong / total_buses)
	print("Total:", total_buses)
result_dir = sys.argv[1]
get_stats(result_dir)