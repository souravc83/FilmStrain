"""
runs script for a beam
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

#reload
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

def plotframestrain(newframeno=setvar.Actuation_Frame,baseframeno=None):
    if baseframeno==None:
        baseframeno=setvar.Actuation_Frame;
    thisframe=frame_estimates.frame_estimates(newframeno);
    zeroframe=frame_estimates.frame_estimates(baseframeno);
    
    thisstrain=thisframe.calc_strain();
    zerostrain=zeroframe.calc_strain();
    strain_val=[thisstrain[i]-zerostrain[i] for i in len(thisstrain)];
    x_str=thisframe.x_str;
    scale=setvar.Length/(setvar.xLeft-setvar.xRight);
    x_scaled=[(j-setvar.xLeft)*scale*1000 for j in x_str];
    
    #plotting
    plt.figure()
    plt.plot(x_scaled,strain_val,'b-');
    plt.xlabel("Axial Position[mm]")
    plt.ylabel("Strain Final");
    plt.show();
    filename="straincurve"+str(newframeno)+".txt";
    vid_utils.savefile(x_scaled,strain_val,filename);
    return;


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
    
    
def beam_script():
    #set_up_analysis();
    check_film_shape(setvar.Actuation_Frame);
    #actuation_relaxation('Coarse');
    #actuation_relaxation('Fine');   
    #relaxlogplot.relaxlogplot();
    #cleanupimgdir();

    
def main():
    beam_script();

if __name__ == "__main__":
    main()    
