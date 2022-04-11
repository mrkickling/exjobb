import matplotlib.pyplot as plt

x_fine = []
y_fine = []
x_coarse = []
y_coarse = []

img = plt.imread("map.png")

with open('plot.csv', 'r') as f:
	for line in f.readlines():
		line = line.split(";")
		x_fine.append(float(line[0]))
		y_fine.append(float(line[1]))
		x_coarse.append(float(line[2]))
		y_coarse.append(float(line[3]))

plt.scatter(x_fine, y_fine, c='red')
plt.plot(x_fine, y_fine, c='red')

# Draw lines to show obfuscation
for i in range(len(x_fine)):
	plt.plot([x_fine[i], x_coarse[i]], [y_fine[i], y_coarse[i]], c='blue', linestyle='dotted')

plt.scatter(x_coarse, y_coarse, c='green')

plt.ylabel('Lon')
plt.xlabel('Lat')

plt.show()