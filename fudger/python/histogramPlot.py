"""

Used to generate 6 histograms of values (for Joakim Loxdal MTh)
Expects 6 input arguments were each is a filename for a csv file

"""

import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


def read_values(path):
    values = []
    with open(path, "r") as f:
        for line in f.readlines()[1:]:  # Skip first line as it is a string
            values.append(float(line.rstrip()))
    return values


# Create a random number generator with a fixed seed for reproducibility
rng = np.random.default_rng(19680801)
n_bins = 30


fig, axs = plt.subplots(3, 2, sharey=True, tight_layout=True)

values_1_iteration = read_values(sys.argv[1])
axs[0][0].hist(values_1_iteration, bins=n_bins)
axs[0][0].set_xlim(0, 2500)
axs[0][0].set_xlabel(r"Distance (m) from $p'$ to $p$")
axs[0][0].set_ylabel(r"Number of $p$'s")
axs[0][0].set_title(r"Fetch 1 $a$'s for each $p$")

values_10_iterations = read_values(sys.argv[2])
axs[0][1].hist(values_10_iterations, bins=n_bins)
axs[0][1].set_xlim(0, 2500)
axs[0][1].set_xlabel(r"Distance (m) from $p'$ to $p$")
axs[0][1].set_ylabel(r"Number of $p$'s")
axs[0][1].set_title(r"Fetch 10 $a$'s for each $p$")

values_100_iteration = read_values(sys.argv[3])
axs[1][0].hist(values_100_iteration, bins=n_bins)
axs[1][0].set_xlim(0, 2500)
axs[1][0].set_xlabel(r"Distance (m) from $p'$ to $p$")
axs[1][0].set_ylabel(r"Number of $p$'s")
axs[1][0].set_title(r"Fetch 100 $a$'s for each $p$")

values_1000_iterations = read_values(sys.argv[4])
axs[1][1].hist(values_1000_iterations, bins=n_bins)
axs[1][1].set_xlim(0, 2500)
axs[1][1].set_xlabel(r"Distance (m) from $p'$ to $p$")
axs[1][1].set_ylabel(r"Number of $p$'s")
axs[1][1].set_title(r"Fetch 1,000 $a$'s for each $p$")

values_10000_iterations = read_values(sys.argv[5])
axs[2][0].hist(values_10000_iterations, bins=n_bins)
axs[2][0].set_xlim(0, 2500)
axs[2][0].set_xlabel(r"Distance (m) from$p'$ to $p$")
axs[2][0].set_ylabel(r"Number of $p$'s")
axs[2][0].set_title(r"Fetch 10,000 $a$'s for each $p$")

values_100000_iterations = read_values(sys.argv[6])
axs[2][1].hist(values_100000_iterations, bins=n_bins)
axs[2][1].set_xlim(0, 2500)
axs[2][1].set_xlabel(r"Distance (m) from $p'$ to $p$")
axs[2][1].set_ylabel(r"Number of $p$'s")
axs[2][1].set_title(r"Fetch 100,000 $a$'s for each p")


plt.show()
