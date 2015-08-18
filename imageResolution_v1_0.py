#------------------------------------------------------------------------------
# Name:         PixResolution.py
# Purpose:      Simple spatial resolution calculator for nadir aerial imagery.
#                   This script has two options, working forward from the 
#                   flying heights to give pixel resolutions or working 
#                   backward from the required pixel resolutions to give flying 
#                   heights. The inputs are given in the console window and the
#                   results are saved to a CSV file in the current working
#                   directory (where the pthon file is located).
#                   Limitations:
#                   1) This script is only for nadir (downward-facing) imagery.
#                       Once you get away from nadir (low or high oblique) 
#                       pixel resolutions change with the depth of field (i.e. 
#                       the pixels close to the camera have a higher spatial 
#                       resolution than the pixels far away). That being said, 
#                       this script can be used to get a ballpark estimate for
#                       low-oblique imagery.
#                   2) It only works for standard cameras, and will not work 
#                       for super wide angle lens (e.g. GoPros or the wide 
#                       angle lenses on the early DJI Phantom platforms). As 
#                       an rule-of-thumb, the horizontal field of view for your
#                       camera should be 70 degrees or less.
#                   ***Obligatory disclaimer...
#                       The calculations are basic trigonometric functions that
#                       do not take into account other variables like lens 
#                       distortion. Given the wide range of potential cameras 
#                       the calculated values should be treated as estimates 
#                       and not as absolute truth.
#
# Compatibility: Python 2.7
#
# Author:       James Dietrich, Dartmouth College
#               james.t.dietrich@dartmouth.edu
# Created:      10 AUG 2015
# Copyright:    (c) James Dietrich 2015
# Licence:      MIT
#
# Useage:       Run this script from the command line or an editor. Enter the
#                   values for each prompt. The calculations in this script are
#                   unit independant, but all linear distance values
#                   (e.g. resolutions or flying heights) need to be in the same
#                   units (feet, meters, whatever you like...).
# Website:      
# http://adv-geo-research.blogspot.com/2015/08/calc-spatial-resolutions-aerial.html
#------------------------------------------------------------------------------

import os
import math
import csv

# funtion to check if a raw_input value is float
# Inputs = a single value (in this case, ususally a string)
def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
# END def isFloat
#-----------
        
# function to calculate the required flying heights and IFOV to achieve the 
# desired pixel resolutions.
# Inputs: sensor dimensions (pixelX,pixelY), camera FOV (xAngle,yAngle),
#         list of required resolutions (req_res)
def calc_AGL(pixelX,pixelY,xAngle,yAngle,req_res):
    
    # Setup vars
    i = 0
    req_AGL = []
    ifov_X = []
    ifov_Y = []  
    
    # for each value in the resolution list calculate the AGL values for both
    # the X & Y dimensions, average the X & Y values as the AGL for the
    # resolution value. Calculate the IFOV for the given AGL value 
    while i < len(req_res):
        
        req_AGL_X = (pixelX * req_res[i] * (1/math.tan(math.radians(
                    xAngle/2))))/200
        req_AGL_Y = (pixelY * req_res[i] * (1/math.tan(math.radians(
                    yAngle/2))))/200
        req_AGL.append((req_AGL_X + req_AGL_Y)/2)
        
        ifov_X.append(2 * (math.tan(math.radians(0.5 * xAngle)) * req_AGL[i]))
        ifov_Y.append(2 * (math.tan(math.radians(0.5 * yAngle)) * req_AGL[i]))
        
        i+=1    # incrument counter
        
    return req_AGL,ifov_X,ifov_Y
# END def calc_AGL
#-----------
    
# function to calculate the IFOV and Pixel resolution for each flying height 
# in a list of flying heights.
# Inputs: sensor dimensions (pixelX,pixelY), camera FOV (xAngle,yAngle),
#         list of flying heights (AGL)
def calc_Res(pixelX,pixelY,xAngle,yAngle,AGL):
    
    # setup vars
    i = 0
    pixResolution_out = []
    ifovX_out = []
    ifovY_out = []
    
    while i < len(AGL):
        
        # Calc IFOV, based on right angle trig of one-half the lens angles
        fov_X = 2 * (math.tan(math.radians(0.5 * xAngle)) * AGL[i])
        fov_Y = 2 * (math.tan(math.radians(0.5 * yAngle)) * AGL[i])
        
        # Write IFOV values to lists
        ifovX_out.append(fov_X)
        ifovY_out.append(fov_Y)
        
        # Calc pixel resolutions based on the IFOV and sensor size     
        pixelResX = (fov_X / pixelX) * 100
        pixelResY = (fov_Y / pixelY) * 100
        
        #Average the X and Y resolutions
        pixResolution_out.append((pixelResX + pixelResY) / 2)
        
        i+=1    # incrument counter
        
    return pixResolution_out, ifovX_out, ifovY_out
# END def calc_Res
#-----------
    
# function to save CSV for Option = 1 (calc pixel resolutions for a range of 
# AGL values). Open CSV file and write Project name, AGL values, corresponding
# pixel resolutions, horizontal and vertical IFOV values.
# Inputs: Prject Name and Units (proj_name,proj_units), list of flying heights 
#        (AGL), calculated pixel resolutions (pixRes), calculated camera IFOV
#        (ifovX_out,ifovY_out)
def save_csvAGLList(proj_name,proj_units,AGL,pixRes,ifovX_out,ifovY_out): 
    # write out csv file with data
    # the file will be in the same directory as this python file
    with open('PixResolution.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["%s" %(proj_name)])
        writer.writerow(['AGL (%s)'%(proj_units)] + AGL)
        writer.writerow(['Pixel Resolution (%s)'%(proj_units)] + pixRes)
        writer.writerow(['IFOV Horz (%s)'%(proj_units)] + ifovX_out)
        writer.writerow(['IFOV Vert (%s)'%(proj_units)] + ifovY_out)
    
    print "Saved to " + os.getcwd() + "\\PixResolution.csv"
# END def save_csvAGLList
#-----------   
    
# function to save CSV for Option = 2 (calc AGL from a range of pixel 
# resolutions). Open CSV file and write Project name, AGL values, pixel 
# resolutions, horizontal and vertical IFOV values.
# Inputs: Prject Name and Units (proj_name,proj_units), calc'd flying heights 
#        (AGL), pixel resolutions (pixRes), calculated camera IFOV
#        (ifovX_out,ifovY_out)
def save_csvResList(proj_name,proj_units,AGL,pixRes,ifovX_out,ifovY_out): 
    # write out csv file with data
    # the file will be in the same directory as this python file
    with open('AGL_Resolution.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["%s" %(proj_name)])
        writer.writerow(['AGL (%s)'%(proj_units)] + AGL)
        writer.writerow(['Pixel Resolution (%s)'%(proj_units)] + pixRes)
        writer.writerow(['IFOV Horz (%s)'%(proj_units)] + ifovX_out)
        writer.writerow(['IFOV Vert (%s)'%(proj_units)] + ifovY_out)
    
    print "Saved to " + os.getcwd() + "\\AGL_Resolution.csv"
# END def save_csvResList
#-----------    

# MAIN

# Print program name and version, get user input for projent name and units
print "\nPixel Resolution Calculator, ver.1.0 (Aug 2015)\n"
proj_name = raw_input("Enter a name(camera type) for this calculation: ")
proj_units = raw_input(
                "Enter the units for your calculations (feet or meters): ")

# User input for type of calculation with error checking, only 1 and 2 are 
# allowed. Continue in a loop until 1 or 2 is entered.
while True:
    print "What would you like to calculate?"
    print "Enter 1 for resolution(s) for a given flying height(s)"
    print "Enter 2 for flying height(s) needed to achieve a specific resolution(s)"
    option = raw_input(" Option = ")
    if option.isdigit():
        if int(option) == 1 or int(option) == 2:
            print " "
            break
        else:
            print "Try again..."
    else:
        print "Try again..."
        
# User input for number of pixels on the sensor. Error check that the inputs
# are float values. Continue in a loop until all values are float.
while True:
    print "Enter the number of pixels on the sensor (take from image dimensions)-"
    pixelX = raw_input(" X (horz) pixels: ")
    pixelY = raw_input(" Y (vert) pixels: ")
    if isFloat(pixelX) and isFloat(pixelY):
        pixelX = float(pixelX)
        pixelY = float(pixelY)
        print "\n"
        break 
    else:
        print "***X and Y dimensions need to be numbers, please try again\n"

# User input for exact field of view angles (FOVs). Error check that the inputs
# are float values. Continue in a loop until all values are float.
# (If unknown, scour the web the answer is out there...)
while True:
    print "Enter the field of view for the lens (take from image dimensions)-"
    xAngle = raw_input(" X (horz) angle: ")
    yAngle = raw_input(" Y (vert) angle: ")
    if isFloat(xAngle) and isFloat(yAngle):
        xAngle = float(xAngle)
        yAngle = float(yAngle)
        print "\n"
        break 
    else:
        print "***X and Y dimensions need to be numbers, please try again\n"

# User input for Option = 1 (calc pixel resolutions for a range of AGL values)
# Split user input at commas and error check that the inputs are float values.
# Continue in a loop until all values are float.
# Call calc_Res to preform calculations and then save_csvAGLList to output
# the results.
if int(option) == 1:
    while True:    
        print "Enter a list of flying height(s) above ground level (AGL) to calculate"
        print "separate multiple entries with commas(,)"
        AGL_str = raw_input(" AGL = ")
        AGL_list = AGL_str.split(",")
        c = [isFloat(item) for item in AGL_list]
        if c.count(True) == len(AGL_list):
            AGL = [float(item) for item in AGL_list]
            AGL.sort()
            
            print "\nYour AGL values were:", AGL, "\n"
            
            [pixResolution_out, ifovX_out, ifovY_out] = calc_Res(
                pixelX,pixelY,xAngle,yAngle,AGL)
                
            save_csvAGLList(
            proj_name,proj_units,AGL,pixResolution_out,ifovX_out,ifovY_out)
            
            break
        else:
            print "***One or more AGL values were not numeric, please try again\n"

# User input for Option = 2 (calc AGL from a range of pixel resolutions)
# Split user input at commas and error check that the inputs are float values.
# Continue in a loop until all values are float.
# Call calc_AGL to preform calculations and then save_csvResList to output
# the results.
elif int(option) == 2:
    while True:
        print "Enter the required resolution(s) in %s: " %(proj_units)
        print "separate multiple entries with commas(,)"
        req_res_str = raw_input(" Resolution(s): ")
        req_res_list = req_res_str.split(",")
        c = [isFloat(item) for item in req_res_list]
        if c.count(True) == len(req_res_list):
            req_res = [float(item) for item in req_res_list]
            req_res.sort()
            
            [req_AGL,ifov_X,ifov_Y] = calc_AGL(
                                        pixelX,pixelY,xAngle,yAngle,req_res)
            save_csvResList(proj_name,proj_units,req_AGL,req_res,ifov_X,ifov_Y)

            break
        else:
            print "***Your required resolution is not numeric, please try again\n"
    
