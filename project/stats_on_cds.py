"""
This is a demo 
for the Python-in-the-lab course
to illustrate how a simple project
can be structured

The final goal is to plot the different Departments
to which the students of the Python course
belong to.
This is done calling the class
Plot_cds_stats twice,
using pie and bar plots
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import classroom as cl 
import customplots as cp


class Plot_cds_stats:
    """
    class to print the data about the students
    """
    def __init__(self, mainDir, csv_filename, cds_filename):
        # Call the Classroom class from classroom.py
        my_class = cl.Classroom(mainDir, csv_filename, cds_filename)
        # cds: codes of Polito Departments
        cds = sorted(my_class.cds)
        self.students = [my_class.get_students_cds(c) for c in cds]
        # Only the first 3 elements of the Departments code are needed
        self.labels = [c[:3] for c in cds]
    
    def pie(self, ax, explode=0.03):
        """
        plot a pie plot using axis ax
        """
        this_plot = cp.CustomPlots(ax)
        if explode is not None:
            if type(explode)  == float:
                # Let's explode all the pies with the same value
                explode = explode * np.ones(len(self.students))
        # Draw the plot
        this_plot.plot_pie(size=self.students, labels=self.labels, explode=explode)
    
    def bar(self, ax):
        """
        plot a bar plot using axis ax
        """
        this_plot = cp.CustomPlots(ax)
        # Draw the plot
        this_plot.plot_bar(size=self.students, labels=self.labels)


if __name__ == "__main__":
    # The plot is setup here, and not in the classes 
    fig, ax = plt.subplots(1,2, figsize=(18,8))
    # Load the file with the students' info
    mainDir = "/home/gf/src/Python/Python-in-the-lab/project"
    csv_file = "01RONKG_2017.csv"
    cds_file = "phds.txt"
    # Initialize the class to plot
    plot = Plot_cds_stats(mainDir, csv_file, cds_file)
    plot.pie(ax[0], explode=0.03)
    plot.bar(ax[1])
    plt.show()