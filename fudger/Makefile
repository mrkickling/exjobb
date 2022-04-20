build:
	javac -d build java/*.java

clean:
	rm build/locationfudger/*.class

plot:
	java -cp build locationfudger/Test | python3 python/plotit.py

plot-offset:
	java -cp build locationfudger/Test | python3 python/plotoffset.py

hack:
	java -cp build locationfudger/Test > out/plot.csv
	python3 python/approxToPrecise.py

build-and-plot: build plot

build-and-plot-offset: build plot-offset

build-and-hack: build hack
