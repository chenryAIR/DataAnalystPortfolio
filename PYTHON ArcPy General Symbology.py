import arcpy
import pandas as pd
import numpy as np


proj = arcpy.mp.ArcGISProject('CURRENT')  #Using the project currently open
m = proj.activeMap   #Use the map currently open
PathDB = proj.defaultGeodatabase   #ArcGIS will default to the Geodatabase created with the project
                                    #PathDB will set a variable to this. On occaision, some code works better if you specifiy it

arcpy.env.overwriteOutput = True  #Tells it to allow for overwriting
arcpy.env.workspace = proj.defaultGeodatabase  #Not really needed because the workspace defaults here, but I do this just in case

#^^^^^^^^^^^^^NOTHING ABOVE THIS LINE NEEDS TO CHANGE FOR THE COMMON LAYER^^^^^^^^^^^^

#------------SET UP THE SYMBOLOGY VARIABLE COLORS AND ROUNDING--------------------------------------

#what variable will be symbolized
sym_var = 'Variable_to_be_symbolized'
#The variable's alias (what will it look like in the legend, popups, etc.)
sym_alias = 'Variable alias' 

#Edit colors -- Fourth number is opacity;
    #Fill Color 
colorP =  [[237, 248, 233, 100],
          [186, 228, 179, 100],
          [116, 196, 118, 100],
          [49, 163, 84, 100],
          [0, 109, 44, 100]]
    #Border color 
colorB =  [[100, 100, 100, 100],
          [100, 100, 100, 100],
          [100, 100, 100, 100],
          [100, 100, 100, 100],
          [100, 100, 100, 100]]

#Round the values(0 == whole number, 1 == tenths, etc.)
roundVal = 0
#Value to increase by (if whole, increase by 1; if 1 decimal, increase by .1; etc. )
roundInc = 1

#--------SET UP WHERE THE DATA COMES FROM---------------------------------------
path = r'H:\share\GIS Methods Group'  #sometimes we'll want to move files, etc. Or the drive will look different locally

#The cleaned file with all the variables you'll you need to map
input = fr'{path}\project_name\file_name.csv'
input_id = 'input_id' #The variable you'll use to join to the shapfile (polygon only)
lat_var = 'latitude_variable' #point only
long_var = 'longitude_variable' #point only

#Where the shapefile is
shapefile = fr'{path}\Census Shapefiles\Unified SD 2019\shapefile_name.shp' #(polygon only)
shapefileID = 'shapefile_id' #The variable you'll use to join with the cleaned data (polygon only)

#++++++++++++++2 Potential pathways. Points or polygons++++++++++++++++++++++++++
#What will you call the new layer made
layerN = 'Layer_Name'

#1.) Points

#The latitude and longitude will be included--Geocoding will be part of the data cleaning process. 
arcpy.management.XYTableToPoint(input, layerN, long_var, lat_var)  #Note: All variables determined above

#2.) Polygons
#you'll have to merge this with an already made shapefile

#import shapefile
arcpy.Select_analysis(shapefile, layerN, "Optional SQL statement")
    #Note: shapefile, layerN were determined above
    #Optional SQL: You can filter a shapefile before you import it.Ex. "STATEFP = '21'" 
        #This will filter the county file for KY (FIPS ==21)
        #leave out if no filter

#Sometimes the ID in the cleaned data won't be the same type as in the shapefile
    #Most often, it'll be a string in the shapefile we'll have to change into a number
#add new variable
new_var = 'ID_new'  #What you will call the new ID variable you'll add to the shapefile for the merge, this doesn't have to change
arcpy.management.AddField(layerN, new_var, 'LONG') #All variables determined above 
    #LONG is the numeric variable type we usually use, use FLOAT if it's really long
#Calculate the new numeric var
arcpy.management.CalculateField(layerN, new_var ,shapefileID) #All variables determined above
arcpy.JoinField_management(layerN, new_var, input, input_id) #All variables determined above

#BOTH.)

#Change the alias of the symbolized variable
arcpy.management.AlterField(layerN, sym_var, new_field_alias = sym_alias)

lyr = m.listLayers(layerN)[0] 
sym = lyr.symbology 
sym.updateRenderer('GraduatedColorsRenderer')
sym.renderer.classificationField = sym_var
sym.renderer.classificationMethod = "Quantile"

x = 0
for brk in sym.renderer.classBreaks:
    if x == 0:
        UB= round(brk.upperBound,roundVal)
        brk.label = "\u2264{0:,.{rv}f}".format(UB, rv = roundVal) #If you need to make changes to the range labels, this is the  first one

    else:
        LB = round(UB + roundInc,roundVal)
        UB= round(brk.upperBound,roundVal)    
        if UB < 0:
            dashTo = " to "
        else: 
            dashTo = " - "
        brk.label = "{0:,.{rv}f}{1}{2:,.{rv}f}".format(LB,dashTo, UB, rv = roundVal) #If you need to make changes to the range labels, this does all but the first one

    
    brk.symbol.color = {'RGB' : colorP[x]}
    brk.symbol.outlineColor = {'RGB' : colorB[x]}
    x = x+1

lyr.symbology  = sym



