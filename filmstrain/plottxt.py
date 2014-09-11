import numpy as np
import matplotlib.pyplot as plt
import os

def plottxt(filename):
    """
    @param filename: String with name of the file
    """
    if (os.path.isfile(filename)==False):
        print "File does not exist";
        return;
    A=np.loadtxt(filename);
    plt.plot(A[:,0],A[:,1],'bo');
    return;
    
     
    