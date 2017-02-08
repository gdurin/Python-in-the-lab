import glob, os, sys
import numpy as np
import matplotlib.pylab as plt

class Dist:
    """
    This class load the data for a single freq and a single type
    """
    def __init__(self, filename, is_avoid_zeros=True):
        # It is better to make general x,y arrays
        self.x, self.y = np.loadtxt(filename, comments="#", unpack=True)
        if is_avoid_zeros:
            s_len = len(self.x)
            self.x, self.y = self.avoid_zeros()
            print("%i lines deleted" % (s_len - len(self.x)))
    
    def avoid_zeros(self):
        is_not_zero = self.y != 0
        x = self.x[is_not_zero]
        y = self.y[is_not_zero]
        return x, y

    def plot(self, loglog=True):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        if loglog:
            ax.loglog(self.x, self.y, 'o')
        else:
            ax.plot(self.x, self.y, 'o')

class DistCollector:
    """
    this is class to collect the filenames 
    in a dictionary

    Parameters:
    ===========
    mainDir: str
        Directory containing the files
    maxLex: int, opt
        max lenght of string describing the file types to consider
        such in F64ac_freq_filetype.dat
    """
    def __init__(self, mainDir, maxLen=1, material="F64ac"):  
        self._mainDir = mainDir
        # Check if the dist_type exists
        # How can we do it?
        dis_types = self.get_distribution_types(maxLen)
        print(dis_types)
        self.distrs = dict()
        for dis_type in dis_types:
            pattern = "%s_????_%s.dat" % (material, dis_type)
            pattern = os.path.join(self._mainDir, pattern)
            filenames = sorted(glob.glob(pattern))
            print(filenames)
            for filename in filenames:
                fname = os.path.join(self._mainDir, filename)
                freq = fname.split("_")[1]
                self.distrs[(dis_type, freq)] = Dist(fname)

    def get_distribution_types(self, maxLen=1):
        filenames = glob.glob(os.path.join(self._mainDir, "*.dat"))
        filenames = [os.path.splitext(filename)[0] for filename in filenames]
        filenames = [filename.split("_", 2)[2] for filename in filenames]
        dis_types = [filename for filename in filenames if len(filename) <= maxLen]
        dis_types = set(dis_types)
        return dis_types

    def plot(self, dis_type, loglog=True):
        # Method to plot all the frequenicies together
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for key in self.distrs:
            if dis_type in key:
                d = self.distrs[key]
                ax.loglog(d.x, d.y, 'o') 
        plt.show()

if __name__ == "__main__":
    mainDir = "/home/gf/src/Python/Python-in-the-lab/Bk"
    dcoll = DistCollector(mainDir)