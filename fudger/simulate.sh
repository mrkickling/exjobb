
# Create a csv file ($2 gives path), $1 gives N (times to fetch approx locations)
# Generate a new precise location 1000 times
# Output the distance from each approximate location to the precise one (into csv file).

echo "distance\n" >> $2
for i in {0..1000}
do
	java -cp build locationfudger/Test standStill $1 | python3 python/approxToPrecise.py >> $2
done