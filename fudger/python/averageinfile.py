import sys

cum_sum = 0
num = 0

with open(sys.argv[1], 'r') as f:
	for line in f.readlines():
		value = float(line)
		cum_sum += value
		num += 1

print(cum_sum / num)