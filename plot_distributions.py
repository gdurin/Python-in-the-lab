import os
import sys
import glob
import matplotlib.pylab as plt
import numpy as np

mainDir = "/home/gf/src/Python/Python-in-the-lab/Bk"


if not os.path.isdir(mainDir):
    print("Houston, we have a problem!")
    sys.exit()

# Let's define a dictionary
distributions = dict()
# This works as well
distributions = {}

distributions['Duration'] = ['T', 'Duration T (s)', r'$P(T)$']
distributions['Size'] = ['S', 'Size S (Wb)', r'$P(S)$']
distributions['Energy'] = ['E', 'Energy E (xx)', r'$P(E)$']

    
def plot_dis(distribution_type, scale='log', ax=None):
    """
    This is my first comment
    This function plot a distribution of my choice
    Parameters:
    distribution_type: str
        The distribution you want to plot
    """
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    ax.set_xscale(scale)
    ax.set_yscale(scale)

    symb, xlabel, ylabel = distributions[distribution_type]

    filenames = sorted(glob.glob1(mainDir, "F64ac_0.0?_%s.dat" % symb))

    for filename in filenames:
        #filename = "F64ac_0.0%i_T.dat" % i # no????
        fname = os.path.join(mainDir, filename)
        x, y = np.loadtxt(fname, unpack=True)
        yerr = y * 0.6
        material, freq, meas = filename.split("_")
        freq = "%s Hz" % freq
        #ax.loglog(x,y,'o', label=freq)
        ax.errorbar(x,y,yerr,fmt='o', label=freq)
    ax.set_xlabel(xlabel, size=16)
    ax.set_ylabel(ylabel, size=16)
    ax.legend()

if __name__ == "__main__":
    my_choice = "Size"
    plot_dis(distribution_type=my_choice)
    plt.show()
