
filename="MP2478";

#Experimental conditions
Intensity=5;
Beam_dia=5e-3;

#Important Frames
Critical_Frame=540;#Not useful for cantilevers
Snapped_Frame=541; #Not useful for cantilevers
Actuation_Frame=43;
Relax_Frame=380;#doesn't mean anything here
End_Relax_Frame=2310;
InitFrame=Actuation_Frame; #This is the frame at which laser switches on


#Cropped Frame to analyze
y_up=330;
y_down=450;
xLeft=225;        
xRight=460;
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
