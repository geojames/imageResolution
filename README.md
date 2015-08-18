# imageResolution
### Simple spatial resolution calculator for nadir aerial imagery.
_Version 1.0 - Initial Release_

This script has two options, working forward from the 
flying heights to give pixel resolutions or working 
backward from the required pixel resolutions to give flying 
heights. The inputs are given in the console window and the
results are saved to a CSV file in the current working
directory (where the python file is located).

Limitations:
1. This script is only for nadir (downward-facing) imagery.
	Once you get away from nadir (low or high oblique) 
    pixel resolutions change with the depth of field (i.e. 
    the pixels close to the camera have a higher spatial 
    resolution than the pixels far away). That being said, 
    this script can be used to get a ballpark estimate for
    low-oblique imagery.
    
2. It only works for standard cameras, and will not work 
    for super wide angle lens (e.g. GoPros or the wide 
    angle lenses on the early DJI Phantom platforms). As 
    an rule-of-thumb, the horizontal field of view for your
    camera should be 70 degrees or less.
    
_**Obligatory disclaimer**_
The calculations are basic trigonometric functions that do not take into account other variables like lens distortion. Given the wide range of potential cameras the calculated values should be treated as estimates and not as absolute truth.
	
Useage:
Run this script from the command line or an editor. Enter the values for each prompt. The calculations in this script are unit independent, but all linear distance values 
(e.g. resolutions or flying heights) need to be in the same units (feet, meters, whatever you like...).
![](https://github.com/geojames/imageResolution/blob/master/nadir_vs_oblique.png)
