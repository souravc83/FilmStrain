"""
@author:Sourav Chatterjee
@brief: calculates time evolution estimates
"""

#import from standard library
import matplotlib.pyplot as plt


#local module imports
import setvar
reload(setvar)
import frame_estimates
reload(frame_estimates)
from vid_utils import savefile


class time_evolution:
    """
    
    """
    def __init__(self,initframe=0,finalframe=setvar.End_Relax_Frame,Interval=10):
        self.initframe=initframe;
        self.finalframe=finalframe;
        self.Interval=Interval;
        
        self.framelist=range(self.initframe,self.finalframe,self.Interval);
        
    def strain_expectation(self,filename='testfile.txt'):
        strain_av=[];
        #strain_dev=[];#std deviation of strain value
        
        #initial frame
        init_frame=frame_estimates.frame_estimates(setvar.Actuation_Frame);
        init_strain_av=init_frame.get_av_strain();
        
        for frame in self.framelist:
            print frame;
            thisframe=frame_estimates.frame_estimates(frame);
            strain_av.append(thisframe.get_av_strain()-init_strain_av);
            #strain_dev.append(thisframe.get_strain_dev());
        
        plt.plot(self.framelist,strain_av,'bo');
        #plt.errorbar(self.framelist,strain_av,yerr=strain_dev,'bo');
        plt.show();
        savefile(self.framelist,strain_av,filename);
        return;
            
            
            
        
        
        