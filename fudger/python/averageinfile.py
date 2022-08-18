import sys

cum_sum = 0
num = 0

for line in sys.stdin:
	value = float(line)
	cum_sum += value
	num += 1

print(cum_sum / num)