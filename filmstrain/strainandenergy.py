from __future__ import division

#import local modules
import setvar
import filmimg 

#import modules from standard library
import numpy as np
#import statistics
import matplotlib.pyplot as plt


class strainandenergy:
    def __init__(self,xfilm,film):
        self.xfilm=xfilm;
        self.film=film;
        self.poly_n=setvar.poly_n;
        self.thickness=setvar.Thickness;
        self.scale=1;
        self.isLshaped=False;
        self.width=setvar.Width;
        self.Youngs_mod=setvar.Youngs_mod;
        self.length=setvar.Length;
        
    
    def setscale(self,scale):
        self.scale=scale;#mm/pixel
        return;
    
    def setLshaped(self,middle,width1,width2):
        self.isLshaped=True;
        self.middle=middle;
        self.width1=width1;
        self.width2=width2;
        return;
    
    def curvatures(self):
        #smooth trace
        self.smoothpoly=np.polyfit(self.xfilm,self.film,self.poly_n);
        self.smoothfilm=np.polyval(self.smoothpoly,self.xfilm);
        
        #find curvature
        p0=np.poly1d(self.smoothpoly);
        p1=np.polyder(p0,1);
        p2=np.polyder(p0,2);
        firstder=p1(self.xfilm);
        secder=p2(self.xfilm);
        N=len(self.xfilm);
        self.curvature=[];
        for i in range(0,N):
            self.curvature.append(secder[i]/((1.+firstder[i]**2.)**1.5));
        return;
        
        
    def calcstrain(self):
        self.curvatures();
        self.strain_sc=[x*self.thickness/self.scale for x in self.curvature];
        return self.strain_sc;
    
    def calc_av_strain(self):
        total_pts=len(self.strain_sc);
        
        #cut off points in left 10% and right 10%
        start_pt=int(0.1*total_pts);
        end_pt=int(0.9*total_pts);
        
        #self.av_strain=statistics.mean(self.strain_sc[start_pt:end_pt]);
        #self.strain_dev=statistics.stdev(self.strain_sc[start_pt:end_pt]);
        
        
        counter=0;
        sum_strain=0;
        for pts in range(total_pts):
            if(pts<0.1*total_pts or pts>0.9*total_pts):
                continue;
            counter+=1;
            sum_strain+=self.strain_sc[pts];
            
        av_strain=sum_strain/counter;
        return av_strain;    
    
    #def get_strain_dev(self):
     #   if hasattr(self,'strain_dev')==False:
      #      self.calc_av_strain();
       # return self.strain_dev;
        
    
    def calcenergy(self):
        if(self.isLshaped==True):
            inertia1=self.width1*(self.thickness**3)/12;
            inertia2=self.width2*(self.thickness**3)/12;
        else:
            inertia=self.width*(self.thickness**3)/12;
            
        self.deltax_sc=(self.xfilm[1]-self.xfilm[0])*self.scale;
        self.curvature_sc=[x/self.scale for x in self.curvature];     
        #print max(self.curvature_sc);
        #print min(self.curvature_sc);
        
        if(self.isLshaped==True):
            energy=self.Lenergy(inertia1,inertia2);
        else:
            energy=self.Straightenergy(inertia);
        return energy;
    
    def Lenergy(self,inertia1,inertia2):
        Energy=0;
        N=len(self.xfilm);
        
        for i in range(0,N):
            if(self.xfilm[i]<self.middle):
                Energy+=(self.Youngs_mod*inertia1)*self.deltax_sc*((1./self.curvature_sc[i])**2);
            else:
                Energy+=(self.Youngs_mod*inertia2)*self.deltax_sc*((1./self.curvature_sc[i])**2);
        
        area=self.width1*(self.middle-self.xfilm[0])*self.scale+self.width2*(self.xfilm[-1]-self.middle)*self.scale;
        self.energy_density=Energy/(area*self.thickness);
        
        return Energy;
    
    def Straightenergy(self,inertia):
        Energy=0;
        N=len(self.xfilm);
        
        for i in range(0,N):
                Energy+=(self.Youngs_mod*inertia)*self.deltax_sc/((1./self.curvature_sc[i])**2);
        
        self.energy_density=Energy/(self.width*self.thickness*self.length);
        return Energy;
                                                                                    
    def showafilmwithstrain(self,frameno):
        A1=filmimg.filmimg(frameno);
        plt.figure();
        plt.imshow(A1.img);
        try:
            plt.plot(self.xfilm,self.smoothfilm,'ro');
        except:
            self.curvatures();
            plt.plot(self.xfilm,self.smoothfilm,'ro');
        finally:
           plt.show();
        return;
    
    def getenergydensity(self):
        return self.energy_density;
