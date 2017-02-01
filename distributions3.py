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
    this is class to collect all the filenames 
    in a dictionary of instances

    Parameters:
    ===========
    mainDir: str
        Directory containing the files
    maxLex: int, opt
        max lenght of string describing the file types to consider
        such in F64ac_freq_filetype.dat
    material: string, opt
        the material used in the experiment
    """
    def __init__(self, mainDir, maxLen=1, material="F64ac"):  
        self._mainDir = mainDir
        # Check if the dist_type exists
        # How can we do it?
        self.dis_types = self._get_distribution_types(maxLen)
        print(self.dis_types)
        self.distrs = dict()
        for dis_type in self.dis_types:
            pattern = "%s_????_%s.dat" % (material, dis_type)
            pattern = os.path.join(self._mainDir, pattern)
            filenames = sorted(glob.glob(pattern))
            print(filenames)
            self.distrs[dis_type] = dict()
            for filename in filenames:
                fname = os.path.join(self._mainDir, filename)
                freq = fname.split("_")[1]
                self.distrs[dis_type][freq] = Dist(fname)

    def plot(self, dis_type, loglog=True):
        if dis_type not in self.dis_types:
            print("Type %s does not exist, please check it" % dis_type)
            return
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for freq in sorted(self.distrs[dis_type]):
            d = self.distrs[dis_type][freq]
            lb = "%s Hz" % freq
            if loglog:
                ax.loglog(d.x, d.y, 'o', label=lb)
            else:
                ax.plot(d.x, d.y, label=lb)
        ax.legend(numpoints=1)
        # Here we need to explicity say to show the plot
        plt.show()

    def _get_distribution_types(self, maxLen=1):
        filenames = glob.glob(os.path.join(self._mainDir, "*.dat"))
        filenames = [os.path.splitext(filename)[0] for filename in filenames]
        filenames = [filename.split("_", 2)[2] for filename in filenames]
        dis_types = [filename for filename in filenames if len(filename) <= maxLen]
        dis_types = set(dis_types)
        return dis_types

if __name__ == "__main__":
    mainDir = "/home/gf/src/Python/Python-in-the-lab/Bk"
    dcoll = DistCollector(mainDir)
    dcoll.plot("S")