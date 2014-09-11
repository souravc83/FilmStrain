"""
@author: Sourav Chatterjee
@brief: contains class for image conversion
"""


#import from standard library
import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage



#import local modules
from vid_utils import plotimage
import setvar
reload(setvar)


#for debugging
import logging
logging.basicConfig(filename='logfile.txt',filemode='w',level=logging.DEBUG)

class filmimg:
    """
    (a)Converts image to black and white
    (b)Applies Gaussian smoothing
    (c)reads image into numpy array
    (d) shows image of film
    """
    def __init__(self,imnum):
        #todo, exception for image does not exist
        self.filename="A/A"+str(imnum)+".jpg";
        self.img=Image.open(self.filename);
        self.gaussian_sigma=setvar.gaussian_sigma;
        self.imgconv(); 
        
        #C++ style construction/initialization
        self.init_ind=0;     
    
    def imgconv(self,applygaussian=True):
        """
        Converts image to black and white
        Reads into numpy array
        @param: applygaussian:Boolean variable stating whether to apply Gaussian smoothing to image
        """
        self.img2=self.img.convert("L");#converts to black and white
        if (applygaussian==True):
            self.A=ndimage.gaussian_filter(self.img2,sigma=self.gaussian_sigma,order=0);
        else:    
            self.A=np.array(self.img2.getdata(),np.uint8).reshape(self.img2.size[1], self.img2.size[0]);
    
    def showfilm(self):
        """
        uses matplotlib to show an image of the film
        """
        #uses plotimage(filename) in vid_utils to plot pixel value 
    
        plotimage(self.filename);
        #Older implementation
        #plt.figure()
        #plt.imshow(self.img);
        #plt.show();


# ....class filmimg ends here...........



class img_features(filmimg):
    """
    Calculates important features from image
    (a) film position
    (b) intensity of an area
    
    """
    def __init__(self,imnum):
        filmimg.__init__(self,imnum); #change this to super()
        self.threshold=setvar.threshold;
        self.X_lim=self.A.shape[1];
        self.Y_lim=self.A.shape[0];
    
    def within_image_x(self,xval):
        
        if(xval>=0 and xval<self.X_lim):
            return True;
        else:
           return False;
          
    def within_image_y(self,yval):
        
        if(yval>=0 and yval<self.Y_lim):
            return True;
        else:
           return False
                                             
    def findmaxinten_x(self,xval,y_up,y_down):
        """
        Finds pixel with maximum intensity
        given x-value, scans y-direction
        @param: xval: int pixel x-location at which scanning happens
        @param: y_up: int pixel y-location to start scanning
        @param: y_down: int pixel y-location to stop scanning
        """
        #todo
        #test within_image
        brightest_ind=y_up+np.argmax(self.A[y_up:y_down,xval]);
        pix_val=self.A[brightest_ind,xval];
        
        return [brightest_ind,pix_val];
    
    def findmaxinten_y(self,x_left,x_right,yval):
        """
        Finds pixel with maximum intensity
        given y-value, scans x-direction
        """
        #todo
        #test within_image
        brightest_ind=x_left+np.argmax(self.A[yval,x_left:x_right]);
        pix_val=self.A[yval,brightest_ind];
        return [brightest_ind,pix_val];
   
    def area_inten(self,x_ul,y_ul,x_br,y_br):#ul is upper left, br is bottom right    
        """
        find total pixel intensity of given area
        """
        #todo
        #test within_image   
        sum=0;
        for i in range(x_ul,x_br):
            for j in range(y_ul,y_br):
                sum=sum+self.A[j,i];
        return sum;
   
    def film_shape(self,x_str,y_up,y_down):
        """
        calculates the shape of the film
        @param: x_str: list of int pixel values, at which the film shape is calculated
        @retval: y_str: list of int pixel values, which give the film shape    
        """
        #this is the most crucial piece of the software.
        #will change often depending on the needs
            
        y_str=[self.findmaxinten_x(i,y_up,y_down)[0] for i in x_str]; #pythonic!
        return y_str;
        

    def film_shape_thresholded_x(self,x_str,y_up,y_down):
        """
        calculates the shape of the film
        determines the length of x_str by comparing with a threshold
        can change the length of x_str
        @param: x_str: list of int pixel values, at which the film shape is calculated
        @retval: y_str: list of int pixel values, which give the film shape    
        """    
        #imp. point here: the end we are trying to make is at the startvalue of the x_str
        #so, we have to iterate from end to start and reverse it
                
        endval=x_str[-1]; #this corresponds to region attached to support
        interval=x_str[-2]-x_str[-1];#assuming uniform intervals,should have negative value
        startval=0;
        #clear x_str, very important
        #operations on mutable sequences: https://docs.python.org/2.4/lib/typesseq-mutable.html
        del x_str[0:len(x_str)];#this is how to delete mutable sequence, 
       
        y_str=[]
        #going through the list in reverse
        for x_px in range(endval,startval,interval):
            [brightest_ind,pix_val]=self.findmaxinten_x(x_px,y_up,y_down);
            #logging.debug(str(x_px)+","+str( brightest_ind)+","+str( pix_val));
            if(pix_val>self.threshold):
                x_str.append(x_px);
                y_str.append(brightest_ind);
            else:
                break;
        #now reverse the lists again
        x_str.reverse();
        y_str.reverse();
        
        return y_str; #should we put this as input too, to be consistent with function below?
        
    def film_shape_thresholded_y(self,x_str,y_str,xLeft,xRight):
        """
        This helps to calculate film shape for really bent films
        by scanning in the horizontal direction.
        @param: x_str: int list of x_values, which are modified by function
        @param: y_str: int list of y_values, which are modified by function
        """
        starty=y_str[0];
        interval=setvar.xInterval;
        endvaly=self.Y_lim;
        
        #revserse 
        x_str.reverse();
        y_str.reverse();
        
        
        for px_y in range(starty+interval,endvaly,interval):
            [brightest_ind,pix_val]=self.findmaxinten_y(xLeft,xRight,px_y);
            print (str( brightest_ind)+","+str(px_y)+","+str( pix_val));
            if(pix_val>self.threshold):
                x_str.append(brightest_ind);
                y_str.append(px_y);
            else:
                break;
        #now reverse the lists again
        x_str.reverse();
        y_str.reverse();
        
        #do not return anything
        

###Class definition ends here####

#Todo: Better way to do this?

def showafilm(frameno=2):
    A1=img_features(frameno);       
    A1.showfilm();