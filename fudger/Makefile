build:
	javac -d build java/*.java

clean:
	rm build/locationfudger/*.class

plot:
	java -cp build locationfudger/Test | python3 python/plotit.py

plot-offset:
	java -cp build locationfudger/Test | python3 python/plotoffset.py

simulate1:
	java -cp build locationfudger/Test standStill 1 | python3 python/approxToPrecise.py >> ../results/stationary-simulated/sim1.txt

simulate10:
	java -cp build locationfudger/Test standStill 10 | python3 python/approxToPrecise.py >> ../results/stationary-simulated/sim10.txt

simulate100:
	java -cp build locationfudger/Test standStill 100 | python3 python/approxToPrecise.py >> ../results/stationary-simulated/sim100.txt

simulate1000:
	java -cp build locationfudger/Test standStill 1000 | python3 python/approxToPrecise.py >> ../results/stationary-simulated/sim1000.txt

simulate10000:
	java -cp build locationfudger/Test standStill 10000 | python3 python/approxToPrecise.py >> ../results/stationary-simulated/sim10000.txt

simulate100000:
	java -cp build locationfudger/Test standStill 100000 | python3 python/approxToPrecise.py >> ../results/stationary-simulated/sim100000.txt

build-and-plot: build plot

build-and-plot-offset: build plot-offset