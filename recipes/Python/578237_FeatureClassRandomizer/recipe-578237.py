# Name:  FeatureClassRandomizer.py
# Date:  23 July 2012
# Developed by:  Reclamation PNGIS - Boise ID
# Description: Randomizes a featureclass by assigning random, unique IDs
# to a featureclass attribute table.  Allows performing random sample of
# the dataset.
#=======================================================================
#import modules
#-----------------------------------------------------------------------
import random
import arcpy
from arcpy import env
#-----------------------------------------------------------------------
# set variables
#-----------------------------------------------------------------------
inFC = r'C:\GIS_WRKSPC\surface.gdb\pntz_2011'
rFld = 'RID'
#-----------------------------------------------------------------------
# run with it...
#-----------------------------------------------------------------------
arcpy.AddField_management(inFC, rFld, "LONG")
f_cnt = int(arcpy.GetCount_management(inFC).getOutput(0)) + 1
print 'A unique ID is being randomly assigned to each row...'
rlist = range(1,f_cnt)
random.shuffle(rlist)
ir = iter(rlist)
while True:
    try:
        rval = ir.next()
        with arcpy.da.UpdateCursor(inFC, rFld) as rcur:
            for row in rcur:
                row[0] = rval
                rcur.updateRow(row)
                rval = ir.next()
    except StopIteration:
        break
print 'Randomization is complete.'
del rlist
#=======================================================================
