"""
runs script for a cantilever
calculates strain as a function of time
"""


#import from standard library
from __future__ import division
import matplotlib.pyplot as plt

#local module imports
import setvar
reload (setvar) #important, for updated setvar values

#from the filmstrain directory
import filmstrain
from filmstrain import filmimg
from filmstrain import vid_utils
from filmstrain.vid_utils import * #Todo: change * import
from filmstrain import strainandenergy
from filmstrain import frame_estimates
from filmstrain import time_evolution
from filmstrain import relaxlogplot

#reload, just to be safe
reload(filmstrain)
reload(filmimg)
reload(vid_utils)
reload(strainandenergy)
reload(frame_estimates)
reload(time_evolution)
reload(relaxlogplot)


def set_up_analysis(frameno=setvar.Relax_Frame):
    #First create images from video
    #put these in try block
    namestr=setvar.filename;
    createimages(namestr);
    createVideo(namestr);
    
    #Check image to set coordinates
    filmimg.showafilm(frameno);

def check_film_shape(frameno=setvar.Relax_Frame):
    #check pictures to check if film is identified correctly
    reload(setvar)
    testframe=frame_estimates.frame_estimates(frameno);
    testframe.showPicture();
        
def actuation_relaxation(granularity='Coarse'):
    #pass;
    #Calculate expected strain with time
    
    if granularity is 'Coarse':
        interval=100;
    elif granularity is 'Fine':
        interval=10;
    else:
        raise ValueError("granularity must be Coarse or Fine");
    
    #interval=1;
    #relax
    relax_regime=time_evolution.time_evolution(setvar.Relax_Frame,setvar.End_Relax_Frame,interval);
    #actuate
    
    #relax_regime=time_evolution.time_evolution(setvar.Actuation_Frame,setvar.Relax_Frame,interval);
    #relax_regime=time_evolution.time_evolution(setvar.Actuation_Frame,setvar.Actuation_Frame+30,interval);
    
    relax_regime.strain_expectation("strainrelax.txt");
    
    
def cantilever_script():
	#run one line at a time
    #set_up_analysis();
    check_film_shape(setvar.Actuation_Frame);
    #actuation_relaxation('Coarse');
    #actuation_relaxation('Fine');   
    #relaxlogplot.relaxlogplot();
    #cleanupimgdir();

    
def main():
    cantilever_script();

if __name__ == "__main__":
    main()    
