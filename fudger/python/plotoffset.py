import matplotlib.pyplot as plt

x_fine = []
y_fine = []
x_offset = []
y_offset = []

with open('plot.csv', 'r') as f:
	first = True
	for line in f.readlines():
		line = line.split(";")
		if first:
			x_fine.append(float(line[0]))
			y_fine.append(float(line[1]))
			first = False
		x_offset.append(float(line[2]))
		y_offset.append(float(line[3]))

print(x_fine[0], y_fine[0])
figure, axes = plt.subplots()
Drawing_colored_circle = plt.Circle(( x_fine[0] , y_fine[0] ), 0.03 )
 
axes.set_aspect( 1 )
axes.add_artist( Drawing_colored_circle )
plt.title( 'Colored Circle' )

plt.scatter(x_offset, y_offset, c='green')
plt.scatter(x_fine, y_fine, c='red')
#plt.ylabel('Lon')
#plt.xlabel('Lat')

plt.show()