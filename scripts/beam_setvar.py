
filename="MP2478";

#Experimental conditions
Intensity=5;
Beam_dia=5e-3;

#Important Frames
Critical_Frame=540;
Snapped_Frame=541; 
Actuation_Frame=43;
Relax_Frame=380;#doesn't mean anything here
End_Relax_Frame=2310;
InitFrame=Actuation_Frame; #This is the frame at which laser switches on


#Cropped Frame to analyze
y_up=330;
y_down=450;

#Geometric Ends of the beam
x_BeamLeftEnd=100;
x_BeamRightEnd=700;

#xLeft and xRight are the points where laser illumination occurs
#to calculate strain
xLeft=225;        
xRight=460;
#if you want to calculate strains for the whole beam, comment out the above
#and uncomment below
xLeft=x_BeamLeftEnd;
xRight=x_BeamRightEnd;

xMiddle=(xLeft+xRight)/2;
xInterval=10;

#Advanced features
LargeDisplacement=False;
threshold=8;#threshold intensity where film ends


#File Geometry
Length=5.e-3;
Width=1e-3
Thickness=20e-6;
is_LShaped=False;
LeftWidth=3e-3;
RightWidth=1e-3;


#Properties
Youngs_mod=2.5e9

#Order of Polynomial for fitting coefficient
poly_n=5; 

#gaussian smoothing parameter
gaussian_sigma=0;
