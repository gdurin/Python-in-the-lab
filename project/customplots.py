"""
custom plots of pie and bar
"""

import numpy as np


class CustomPlots:
    def __init__(self, ax):
        self.ax = ax

    def plot_xy(self, x, y, marker='o', color='r'):
        self.ax.plot(x, y, mk=marker, cl=color)

    def plot_pie(self, size, labels, explode=None, autopct='%1.1f%%',
        shadow=True, startangle=90):
        patches, texts, autotext = self.ax.pie(size, labels=labels, 
            explode=explode, autopct=autopct, shadow=shadow, 
            startangle=startangle)
        self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        [t.set_fontsize(22) for t in texts]
    
    def plot_bar(self, size, labels, width=0.4):
        x = np.arange(1, len(labels)+1)
        self.ax.bar(x, size, width)
        self.ax.set_ylabel('Students')
        self.ax.set_xticks(x + width / 2)
        self.ax.set_xticklabels(tuple(labels))


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    cp = CustomPlots(ax1)
    cp.plot_pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    plt.show()
