from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

#local module imports
import setvar

def calc_end_index(Y_val):
    counter=0;
    ymin=min(Y_val);
    while(Y_val[counter]!=ymin):
        counter+=1;
    return counter;


def relaxlogplot(filename="strainrelax.txt"):
    B=np.loadtxt(filename);
    #plt.plot(B[:,0],B[:,1],'bo');
    
    fps=7.;
    start1=0;
    #end1=B.shape[0];
    end1=40;
    X_val=(B[start1:end1,0]-B[start1,0])/fps;
    Y_val=B[start1:end1,1];
    #epsilon=1e-12;
    Y_max=max(Y_val);
    #Y_val=[((Y_max-x)/Y_max) for x in Y_val];
    
    
    #end_index=calc_end_index(Y_val);
    #X_val=X_val[0:end_index];
    #Y_val=Y_val[0:end_index];
    Y_val=[math.log(x) for x in Y_val];
    plt.figure();
    plt.plot(X_val,Y_val,'bo');
    
    slope, intercept, r_value, p_value, std_err=stats.linregress(X_val,Y_val);    
    line=slope*X_val+intercept;
    plt.plot(X_val,line,'r-');
    
    error_time=0.5*((1./(slope-std_err))-(1./(slope+std_err)));

    
    print "Irradiation Frames: "+str(setvar.Relax_Frame-setvar.Actuation_Frame);
    
    print "Maximum Strain: "+str(Y_max);
    print "Time Constant: " +str(1/slope)+" +- " +str(error_time);
    print "r-value: "+str(r_value);
    
    plt.show();
    
    
if __name__ == "__main__":
    main()
