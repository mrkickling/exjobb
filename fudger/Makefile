build:
	javac -d build java/*.java

clean:
	rm build/locationfudger/*.class

plot:
	java build/locationfudger/Test > out/plot.csv
	python3 python/plotit.py

plot-offset:
	java build/locationfudger/Test > out/plot.csv
	python3 python/plotoffset.py

hack:
	java build/locationfudger/Test > out/plot.csv
	python3 python/approxToPrecise.py

build-and-plot: build plot

build-and-plot-offset: build plot-offset

build-and-hack: build hack