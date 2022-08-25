import sys
import pandas as pd

# Reads the file name as csv
# The file is supposed to contain distances between locations
filename = sys.argv[1]
file = pd.read_csv(filename)
print(file)

# Statistical analysis
df = file["distance"].std()
avg = file["distance"].mean()
median = file["distance"].median()
min_value = file["distance"].min()
max_value = file["distance"].max()

# Output
print("min", min_value)
print("max", max_value)
print("std dev", df)
print("mean", avg)
print("median", median)
