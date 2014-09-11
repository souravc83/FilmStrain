"""
@author: Sourav Chatterjee
@brief:class estimates strain, energy and other parameters for a single frame
"""

#import from standard library


#local module imports
import filmimg
reload(filmimg)
import setvar
reload (setvar)
import strainandenergy
reload(strainandenergy)

#for debugging
import logging
logging.basicConfig(filename='logfile.txt',level=logging.DEBUG)





class frame_estimates:
    """
    makes all estimates for a given frame
    """
    #this class does all the heavy lifting
    
    def __init__(self,frameno=2,xLeft=setvar.xLeft,xRight=setvar.xRight,xInterval=setvar.xInterval):
        self.frameno=frameno;
        self.img_feature=filmimg.img_features(self.frameno);
        self.xLeft=xLeft;
        self.xRight=xRight;
        self.xInterval=xInterval;
        self.y_up=setvar.y_up;
        self.y_down=setvar.y_down;
        
        
        self.x_str=[];
        self.y_str=[];
        
        self.film_shape();#implementationcan change in future
        self.strainenergy=strainandenergy.strainandenergy(self.x_str,self.y_str);
        scale=setvar.Length/(self.xRight-self.xLeft);
        self.strainenergy.setscale(scale);
        if setvar.is_LShaped==True:
            self.strainenergy.setLshaped(setvar.xMiddle,setvar.LeftWidth,setvar.RightWidth);
        
    
    def film_shape(self):
        self.x_str=range(self.xLeft,self.xRight,self.xInterval);
        if(setvar.LargeDisplacement==False):
            self.y_str=self.img_feature.film_shape(self.x_str,self.y_up,self.y_down);
        else:
            #Warning: the command below changes size of x_str
            self.y_str=self.img_feature.film_shape_thresholded_x(self.x_str,self.y_up,self.y_down);
            #Additional function for almost vertical film, large shape changes
            self.img_feature.film_shape_thresholded_y(self.x_str,self.y_str,self.xLeft,680);
        
        #logging.debug("Returned x size: "+str(len(self.x_str)));
        
        return;
    
    def strain_calc(self):
        self.strain_val=self.strainenergy.calcstrain();
        return;
    
    def energy_calc(self):
        self.energy_val=self.strainenergy.calcenergy();
        return;
    
    def energy_density_val(self):
        self.e_den_val=self.strainenergy.getenergydensity();
        return;
    
    def showPicture(self):
        self.strainenergy.showafilmwithstrain(self.frameno);
    
    def get_av_strain(self):
        self.strain_val=self.strainenergy.calcstrain();
        self.av_strain=self.strainenergy.calc_av_strain();
        return self.av_strain;
    
    #def get_strain_dev(self):
     #   return self.strainenergy.get_strain_dev();
        
        
            